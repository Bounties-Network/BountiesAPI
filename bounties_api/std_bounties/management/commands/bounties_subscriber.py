import time
import logging
import pprint
import re

from django.core.management.base import BaseCommand
from django.conf import settings
from ipfsapi.exceptions import StatusError
from botocore.exceptions import ClientError

from bounties.redis_client import redis_client
from bounties.sqs_client import sqs_client
from std_bounties import master_client
from std_bounties.models import Event
from std_bounties.message import Message
from std_bounties.constants import STANDARD_BOUNTIES_V1, STANDARD_BOUNTIES_V2
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

                already_deduplicated = redis_client.get(message.message_deduplication_id)
                if already_deduplicated and already_deduplicated.decode('UTF-8') == 'True':
                    self.remove_from_queue(message)
                    continue

                # If someone uploads a data hash that is faulty, then we want to blacklist all events around that
                # bounty id. It can either be a permanent blacklist, typically added manually, or a pending blacklist.
                # All the events in the pending blacklist will retry later.
                permanent_blacklist = redis_client.get('blacklist:{}'.format(message.bounty_id))
                pending_blacklist = redis_client.exists('pending_blacklist:{}'.format(message.bounty_id))

                if permanent_blacklist or pending_blacklist:
                    self.remove_from_queue(message)
                    if permanent_blacklist:
                        logger.info('Skipping event for {}, permanent blacklist found'.format(message.bounty_id))
                    else:
                        logger.info('Pending blacklist exists for {}, adding event {}'.format(message.bounty_id, message.event))
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
            logger.warning('SQS delete_message hit an error: '.format(e.response['Error']['Message']))

    def add_to_blacklist(self, message):
        existing = redis_client.lrange('pending_blacklist:{}'.format(message.bounty_id), 0, -1)
        message_string = str(message)

        for key in existing:
            if key and key.decode('UTF-8') == message_string:
                logger.warning('Did not add {} to pending_blacklist, already '
                               'existed'.format(message.bounty_id))
                return

        redis_client.rpush('pending_blacklist:{}'.format(message.bounty_id), message_string)
        logger.warning('Added to {} to pending_blacklist'.format(message.bounty_id))

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
        logger.info('For bounty id {}, running event {}'.format(message.bounty_id, message.event))

        if message.contract_version == STANDARD_BOUNTIES_V1:
            self.notify_master_client(message)
        else:
            self.notify_master_client_v2(message)

        bounty = Bounty.objects.get(bounty_id=message.bounty_id, contract_version=message.contract_version)

        event_arguments = {
            'bounty_id': bounty.pk,
            'fulfillment_id': message.contract_event_data.get('fulfillment_id', None),
            'transaction_from': message.transaction_from,
            'contract_inputs': message.contract_method_inputs,
            'contract_event_data': message.contract_event_data,
            'event_date': message.event_date,
        }

        # logger.info('For bounty id {}, running get_or_create with defaults'.format(message.bounty_id))
        # pp.pprint(event_arguments)

        Event.objects.get_or_create(
            event=message.event,
            transaction_hash=message.transaction_hash,
            defaults=event_arguments
        )

        transaction_path = '/bounty/' + str(bounty.pk)
        transaction_link_text = 'View bounty'
        transaction_message = 'Transaction confirmed'

        if message.event == 'FulfillmentAccepted':
            transaction_path = '{}/?fulfillment_id={}&rating=true'.format(
                transaction_path,
                message.contract_event_data['fulfillment_id']
            )

            transaction_link_text = 'Rate fulfiller'
            transaction_message = 'Submission accepted'

        transactions = Transaction.objects.filter(tx_hash=message.transaction_hash)
        if transactions.exists():
            transactions.update(completed=True, viewed=False, data={
                'link': transaction_path,
                'linkText': transaction_link_text,
                'message': transaction_message,
            })

        #  this should be done in the master / bounty client
        #
        #  if message.event == 'BountyActivated':
        #      is_issue_and_activate = message.contract_method_inputs.get('issuer', None)
        #      if is_issue_and_activate:
        #          slack_client.bounty_issued_and_activated(bounty)
        #          notification_client.bounty_issued_and_activated(
        #              bounty_id,
        #              event_date=message.event_date,
        #              inputs=message.contract_method_inputs,
        #              event_timestamp=message.event_timestamp,
        #              uid=message.message_deduplication_id)
        #      else:
        #          notification_client.bounty_activated(
        #              bounty_id,
        #              event_date=message.event_date,
        #              inputs=message.contract_method_inputs,
        #              event_timestamp=message.event_timestamp,
        #              uid=message.message_deduplication_id)
        #          slack_client.bounty_activated(bounty)
        #
        #  if message.event == 'PayoutIncreased':
        #      bounty = Bounty.objects.get(bounty_id=bounty_id)
        #      notification_client.payout_increased(
        #          bounty_id,
        #          event_date=message.event_date,
        #          inputs=message.contract_method_inputs,
        #          uid=message.message_deduplication_id)
        #      slack_client.payout_increased(bounty)

    def notify_master_client(self, message):
        event = message.event
        inputs = message.contract_method_inputs
        event_data = message.contract_event_data

        print('contract inputs = ', inputs)
        print('event data = ', event_data)

        try:
            base_event_data = {
                'bounty_id': message.bounty_id,
                'contract_version': STANDARD_BOUNTIES_V1,
                'event_date': message.event_date,
                'event_timestamp': message.event_timestamp,
                'uid': message.message_deduplication_id,
            }

            if event == 'BountyIssued':
                master_client.client['bounty_issued'](
                    **base_event_data,
                    **{
                        'creator': inputs.get('issuer'),
                        'issuers': [inputs.get('issuer')],
                        'approvers': [inputs.get('issuer')],
                        'data': inputs.get('data'),
                        'deadline': inputs.get('deadline'),
                        'fulfillment_amount': inputs.get('fulfillmentAmount'),
                        'value': inputs.get('value'),
                        'token': inputs.get('tokenContract'),
                        'token_version': '20' if inputs.get('paysTokens') else '0',
                    },
                )

            elif event == 'BountyActivated':
                master_client.client['bounty_activated'](
                    **base_event_data,
                    **{
                        'issuer': inputs.get('issuer', None)
                    },
                )

            elif event == 'BountyFulfilled':
                master_client.client['bounty_fulfilled'](
                    **base_event_data,
                    **{
                        'fulfillment_id': event_data.get('fulfillment_id'),
                        'fulfillers': [event_data.get('fulfiller')],
                        'submitter': event_data.get('fulfiller'),
                        'data': inputs.get('data'),
                    },
                )

            # untested
            elif event == 'FulfillmentUpdated':
                master_client.client['fullfillment_updated'](
                    **base_event_data,
                    **{
                        'fulfillment_id': event_data.get('fulfillment_id'),
                        'fulfillers': [message.transaction_from],
                        'data': inputs.get('data'),
                    },
                )

            elif event == 'FulfillmentAccepted':
                bounty = Bounty.objects.get(
                    bounty_id=message.bounty_id,
                    contract_version=STANDARD_BOUNTIES_V1,
                )

                master_client.client['fulfillment_accepted'](
                    **base_event_data,
                    **{
                        'fulfillment_id': event_data.get('fulfillment_id'),
                        'token_amounts': [bounty.fulfillment_amount],
                        'approver': message.transaction_from,
                    },
                )

            # untested
            elif event == 'BountyKilled':
                master_client.bounty_killed(
                    **base_event_data,
                )

            elif event == 'ContributionAdded':
                master_client.client['contribution_added'](
                    **base_event_data,
                    **{
                        'contribution_id': 0,
                        'contributor': event_data.get('contributor'),
                        'amount': event_data.get('value'),
                    }
                )

            # untested
            elif event == 'DeadlineExtended':
                master_client.client['bounty_deadline_changed'](
                    **base_event_data,
                    **{
                        'changer': message.transaction_from,
                        'deadline': event_data.get('new_deadline'),
                    },
                )

            elif event == 'BountyChanged':
                # this event only occurs when a draft bounty is edited
                pass

            # untested
            elif event == 'IssuerTransferred':
                master_client.client['bounty_issuers_updated'](
                    **base_event_data,
                    **{
                        'changer': message.transaction_from,
                        'issuers': [event_data.get('new_issuer')],
                    },
                )

                master_client.client['bounty_approvers_updated'](
                    **base_event_data,
                    **{
                        'changer': message.transaction_from,
                        'approvers': [event_data.get('new_issuer')],
                    },
                )

            # untested
            elif event == 'PayoutIncreased':
                master_client.client['payout_increased'](
                    **base_event_data,
                    **{
                        'fulfillment_amount': event_data.get('new_fulfillment_amount'),
                    },
                )

                master_client.client['contribution_added'](
                    **base_event_data,
                    **{
                        'contribution_id': 0,
                        'contributor': message.transaction_from,
                        'amount': inputs.get('value'),
                    }
                )

            else:
                logger.warning('Event for bounty id {} not recognized: {}'.format(message.bounty_id, event))

        except StatusError as e:
            if e.original.response.status_code == 504:
                logger.warning('Timeout for bounty id {}'.format(message.bounty_id))
            raise e

    def notify_master_client_v2(self, message):
        try:
            # make camel case
            event = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', message.event)
            event = re.sub('([a-z0-9])([A-Z])', r'\1_\2', event).lower()

            print(message.contract_event_data)

            events_to_skip = [
                # not relevant for getting stb 2.0 to be compatible with stb 1.0,
                # and this event may change to `bounty_issuers_changed` instead
                # 'bounty_issuers_updated',
                # 'bounty_approvers_updated',
            ]

            if event in events_to_skip:
                return

            master_client.client[event](
                message.bounty_id,
                contract_version=STANDARD_BOUNTIES_V2,
                event_date=message.event_date,
                event_timestamp=message.event_timestamp,
                uid=message.message_deduplication_id,
                **{k: v for (k, v) in message.contract_event_data.items() if 'bounty_id' not in k},
            )
        except StatusError as e:
            if e.original.response.status_code == 504:
                logger.warning('Timeout for bounty id {}'.format(message.bounty_id))
            raise e
