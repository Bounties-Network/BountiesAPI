import time
import logging
import pprint

from django.core.management.base import BaseCommand
from django.conf import settings
from ipfsapi.exceptions import StatusError
from botocore.exceptions import ClientError

from bounties.redis_client import redis_client
from bounties.sqs_client import sqs_client
from std_bounties import master_client
from std_bounties.models import Event
from std_bounties.message import Message
from notifications.models import Transaction

from std_bounties.bounty_client import BountyClient
from notifications.notification_client import NotificationClient
from std_bounties.slack_client import SlackMessageClient
from std_bounties.models import Bounty

bounty_client = BountyClient()
notification_client = NotificationClient()
slack_client = SlackMessageClient()
logger = logging.getLogger('django')
pp = pprint.PrettyPrinter(indent=4)


class Command(BaseCommand):
    help = 'Listen to SQS queue for contract events'

    def add_arguments(self, parser):
        parser.add_argument(
            '--blacklist',
            action='store_true',
            dest='blacklist',
            help='Process blacklisted events',
            default=False
        )

    def handle(self, *args, **options):
        if options['blacklist']:
            self.resolve_blacklist()
            return

        while True:
            try:
                # poll by the second
                if not settings.LOCAL:
                    time.sleep(1)

                # TODO - All should be a transaction atomic function
                response = sqs_client.receive_message(
                    QueueUrl=settings.QUEUE_URL,
                    AttributeNames=['MessageDeduplicationId'],
                    MessageAttributeNames=['All'],
                    MaxNumberOfMessages=1,
                )

                messages = response.get('Messages')
                if not messages:
                    continue

                # There is only ever 1 because MaxNumberOfMessages=1
                message = Message.from_event(messages[0])

                already_deduplicated = redis_client.get(
                    message.message_deduplication_id)
                if already_deduplicated and already_deduplicated.decode('UTF-8') == 'True':
                    self.remove_from_queue(message)
                    continue

                # If someone uploads a data hash that is faulty, then we want to blacklist all events around that
                # bounty id. It can either be a permanent blacklist, typically added manually, or a pending blacklist.
                # All the events in the pending blacklist will retry later.
                permanent_blacklist = redis_client.get(
                    'blacklist:{}'.format(message.bounty_id))
                pending_blacklist = redis_client.exists(
                    'pending_blacklist:{}'.format(message.bounty_id))

                if permanent_blacklist or pending_blacklist:
                    self.remove_from_queue(message)
                    if permanent_blacklist:
                        logger.info('Skipping event for {}, permanent blacklist found'.format(
                            message.bounty_id))
                    else:
                        logger.info('Pending blacklist exists for {}, adding event {}'.format(
                            message.bounty_id, message.event))
                        self.add_to_blacklist(message)
                    continue

                self.handle_message(message)
                self.remove_from_queue(message)

            except Exception as e:
                # goes to rollbar
                logger.error(e)
                self.remove_from_queue(message)
                self.add_to_blacklist(message)

    def remove_from_queue(self, message):
        # This means the contract subscriber will never send this event
        # through to sqs again
        redis_client.set(message.message_deduplication_id, 'True')
        try:
            sqs_client.delete_message(
                QueueUrl=settings.QUEUE_URL,
                ReceiptHandle=message.receipt_handle,
            )
        except ClientError as e:
            logger.warning('SQS delete_message hit an error: '.format(
                e.response['Error']['Message']))

    def add_to_blacklist(self, message):
        existing = redis_client.lrange('pending_blacklist:{}'.format(
            message.bounty_id), 0, -1)

        message_string = str(message)

        for key in existing:
            if key and key.decode('UTF-8') == message_string:
                logger.warning('Did not add {} to pending_blacklist, already '
                               'existed'.format(message.bounty_id))
                return

        redis_client.rpush('pending_blacklist:{}'.format(
            message.bounty_id), message_string)
        logger.warning(
            'Added to {} to pending_blacklist'.format(message.bounty_id))

    def resolve_blacklist(self):
        for key in redis_client.scan_iter('pending_blacklist:*'):
            logger.info(
                'Attempting to pop pending_blacklist queue {}'.format(key))
            try:
                retry = redis_client.lpop(key).decode('UTF-8')
                logger.warning('Retrying event: {}'.format(retry))
                self.handle_message(Message.from_string(retry))
            except Exception as e:
                # Don't re-raise - we just place it back in the list and try
                # again later
                logger.warning('Retrying event for {} failed with {}'.format(
                    key, e))
                redis_client.lpush(key, retry)

    def handle_message(self, message):
        logger.info('For bounty id {}, running event {}'.format(
            message.bounty_id, message.event))

        self.notify_master_client(message)

        fulfillment_id = message.fulfillment_id
        if fulfillment_id == -1:
            fulfillment_id = None

        bounty_id = message.bounty_id
        if bounty_id == -1:
            bounty_id = None

        event_arguments = {
            'bounty_id': bounty_id,
            'fulfillment_id': fulfillment_id,
            'transaction_from': message.transaction_from,
            'contract_inputs': message.contract_method_inputs,
            'event_date': message.event_date,
        }

        logger.info(
            'For bounty id {}, running get_or_create with defaults'.format(
                message.bounty_id))
        pp.pprint(event_arguments)

        Event.objects.get_or_create(
            event=message.event,
            transaction_hash=message.transaction_hash,
            defaults=event_arguments
        )

        transaction_path = '/bounty/' + str(bounty_id)
        transaction_link_text = 'View bounty'
        transaction_message = 'Transaction confirmed'

        if message.event == 'FulfillmentAccepted':
            transaction_path = '{}/?fulfillment_id={}&rating=true'.format(
                transaction_path,
                fulfillment_id)
            transaction_link_text = 'Rate fulfiller'
            transaction_message = 'Submission accepted'

        transactions = Transaction.objects.filter(
            tx_hash=message.transaction_hash)
        if transactions.exists():
            transactions.update(completed=True, viewed=False, data={
                'link': transaction_path,
                'linkText': transaction_link_text,
                'message': transaction_message,
            })

        if message.event == 'BountyActivated':
            bounty = Bounty.objects.get(bounty_id=bounty_id)
            is_issue_and_activate = message.contract_method_inputs.get(
                'issuer', None)
            if is_issue_and_activate:
                slack_client.bounty_issued_and_activated(bounty)
                notification_client.bounty_issued_and_activated(
                    bounty_id,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    event_timestamp=message.event_timestamp,
                    uid=message.message_deduplication_id)
            else:
                notification_client.bounty_activated(
                    bounty_id,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    event_timestamp=message.event_timestamp,
                    uid=message.message_deduplication_id)
                slack_client.bounty_activated(bounty)

        if message.event == 'ContributionAdded':
            bounty = Bounty.objects.get(bounty_id=bounty_id)
            is_issue_and_activate = message.contract_method_inputs.get(
                'issuer', None)
            if not is_issue_and_activate:
                notification_client.contribution_added(
                    bounty_id,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    event_timestamp=message.event_timestamp,
                    transaction_from=message.transaction_from,
                    uid=message.message_deduplication_id)
                slack_client.contribution_added(bounty)

        if message.event == 'PayoutIncreased':
            bounty = Bounty.objects.get(bounty_id=bounty_id)
            notification_client.payout_increased(
                bounty_id,
                event_date=message.event_date,
                inputs=message.contract_method_inputs,
                uid=message.message_deduplication_id)
            slack_client.payout_increased(bounty)

    def notify_master_client(self, message):
        event = message.event
        try:
            if event == 'BountyIssued':
                master_client.bounty_issued(
                    message.bounty_id,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    event_timestamp=message.event_timestamp,
                    uid=message.message_deduplication_id)

            elif event == 'BountyActivated':
                master_client.bounty_activated(
                    message.bounty_id,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    event_timestamp=message.event_timestamp,
                    uid=message.message_deduplication_id)

            elif event == 'BountyFulfilled':
                master_client.bounty_fulfilled(
                    message.bounty_id,
                    fulfillment_id=message.fulfillment_id,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    event_timestamp=message.event_timestamp,
                    transaction_issuer=message.transaction_from,
                    uid=message.message_deduplication_id)

            elif event == 'FulfillmentUpdated':
                master_client.fullfillment_updated(
                    message.bounty_id,
                    event_date=message.event_date,
                    fulfillment_id=message.fulfillment_id,
                    inputs=message.contract_method_inputs,
                    uid=message.message_deduplication_id)

            elif event == 'FulfillmentAccepted':
                master_client.fulfillment_accepted(
                    message.bounty_id,
                    event_date=message.event_date,
                    fulfillment_id=message.fulfillment_id,
                    event_timestamp=message.event_timestamp,
                    uid=message.message_deduplication_id)

            elif event == 'BountyKilled':
                master_client.bounty_killed(
                    message.bounty_id,
                    event_date=message.event_date,
                    event_timestamp=message.event_timestamp,
                    uid=message.message_deduplication_id)

            elif event == 'ContributionAdded':
                master_client.contribution_added(
                    message.bounty_id,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    transaction_from=message.transaction_from,
                    event_timestamp=message.event_timestamp,
                    uid=message.message_deduplication_id)

            elif event == 'DeadlineExtended':
                master_client.deadline_extended(
                    message.bounty_id,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    event_timestamp=message.event_timestamp,
                    uid=message.message_deduplication_id)

            elif event == 'BountyChanged':
                master_client.bounty_changed(
                    message.bounty_id,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    uid=message.message_deduplication_id)

            elif event == 'IssuerTransferred':
                master_client.issuer_transferred(
                    message.bounty_id,
                    transaction_from=message.transaction_from,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    uid=message.message_deduplication_id)

            elif event == 'PayoutIncreased':
                master_client.payout_increased(
                    message.bounty_id,
                    event_date=message.event_date,
                    inputs=message.contract_method_inputs,
                    uid=message.message_deduplication_id)

            else:
                logger.warning('Event for bounty id {} not recognized:'
                               '{}'.format(message.bounty_id, event))

        except StatusError as e:
            if e.original.response.status_code == 504:
                logger.warning(
                    'Timeout for bounty id {}'.format(message.bounty_id))
            raise e
