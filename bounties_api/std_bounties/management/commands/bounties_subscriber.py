import json
import time
import datetime
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from ipfsapi.exceptions import StatusError 

from bounties.redis_client import redis_client
from bounties.sqs_client import sqs_client
from std_bounties import master_client
from std_bounties.models import Event
from std_bounties.message import Message


logger = logging.getLogger('django')

class Command(BaseCommand):
    help = 'Listen to SQS queue for contract events'

    def resolve_blacklist(self):
        logger.info('checking retry_blacklist for entries')
        retry = redis_client.lrange('retry_blacklist', 0, -1)
        for blacklisted in retry:
            logger.info('retrying blacklsited entry: {}'.format(blacklisted))
            blacklisted_message = redis_client.get(blacklisted)
            if blacklisted_message:
                self.handle_message(Message.from_string(blacklisted_message))
                redis_client.lrem('retry_blacklist', 0, blacklisted)

    def handle(self, *args, **options):
        try:
            # retry the blacklisted events when this reaches zero
            retry_blacklist_rate = 200
            retry_blacklist = retry_blacklist_rate

            while True:
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

                # If someone uploads a data hash that is faulty, then we want to blacklist all events around that
                # bounty id. We manage this manually
                if redis_client.get('blacklist:' + str(message.bounty_id)):
                    redis_client.set(message.message_deduplication_id, True)
                    sqs_client.delete_message(
                        QueueUrl=settings.QUEUE_URL,
                        ReceiptHandle=message.receipt_handle,
                    )
                    continue

                self.handle_message(message)

                retry_blacklist -= 1
                logger.info('done processing regular message, retry_blacklist is now: {}'.format(
                    retry_blacklist))

                if retry_blacklist <= 0:
                    retry_blacklist = retry_blacklist_rate
                    logger.info('retry_blacklist reset to: {}'.format(retry_blacklist))
                    self.resolve_blacklist()

        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e

    def handle_message(self, message):
        logger.info('For bounty id {}, running event {}'.format(
            message.bounty_id, message.event))

        self.notify_master_client(message)

        event_arguments = {
            'bounty_id': message.bounty_id,
            'fulfillment_id': message.fulfillment_id if message.fulfillment_id != -1 else None,
            'transaction_from': message.transaction_from,
            'contract_inputs': message.contract_method_inputs,
            'event_date': message.event_date,
        }

        logger.info('For bounty id {}, running get_or_create with defaults: {}'.format(
            message.bounty_id, event_arguments))

        Event.objects.get_or_create(
            event=message.event,
            transaction_hash=message.transaction_hash,
            defaults=event_arguments
        )

        # This means the contract subscriber will never send this event
        # through to sqs again
        redis_client.set(message.message_deduplication_id, True)
        sqs_client.delete_message(
            QueueUrl=settings.QUEUE_URL,
            ReceiptHandle=message.receipt_handle,
        )

    def notify_master_client(self, message):
        event = message.event
        try:
            if event == 'BountyIssued':
                master_client.bounty_issued(message.bounty_id,
                                            event_date=message.event_date,
                                            inputs=message.contract_method_inputs,
                                            event_timestamp=message.event_timestamp)
            elif event == 'BountyActivated':
                master_client.bounty_activated(message.bounty_id,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs,
                                                event_timestamp=message.event_timestamp)
            elif event == 'BountyFulfilled':
                master_client.bounty_fulfilled(message.bounty_id,
                                                fulfillment_id=message.fulfillment_id,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs,
                                                event_timestamp=message.event_timestamp,
                                                transaction_issuer=message.transaction_from)
            elif event == 'FulfillmentUpdated':
                master_client.fullfillment_updated(message.bounty_id,
                                                    event_date=message.event_date,
                                                    fulfillment_id=message.fulfillment_id,
                                                    inputs=message.contract_method_inputs)
            elif event == 'FulfillmentAccepted':
                master_client.fulfillment_accepted(message.bounty_id,
                                                    event_date=message.event_date,
                                                    fulfillment_id=message.fulfillment_id,
                                                    event_timestamp=message.event_timestamp)
            elif event == 'BountyKilled':
                master_client.bounty_killed(message.bounty_id,
                                            event_date=message.event_date,
                                            event_timestamp=message.event_timestamp)
            elif event == 'ContributionAdded':
                master_client.contribution_added(message.bounty_id,
                                                    event_date=message.event_date,
                                                    inputs=message.contract_method_inputs,
                                                    event_timestamp=message.event_timestamp)
            elif event == 'DeadlineExtended':
                master_client.deadline_extended(message.bounty_id,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs,
                                                event_timestamp=message.event_timestamp)
            elif event == 'BountyChanged':
                master_client.bounty_changed(message.bounty_id,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs)
            elif event == 'IssuerTransferred':
                master_client.issuer_transferred(message.bounty_id,
                                                transaction_from=message.transaction_from,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs)
            elif event == 'PayoutIncreased':
                master_client.payout_increased(message.bounty_id,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs)
            else:
                logger.warning('Event for bounty id {} not recognized: {}'.format(
                    message.bounty_id, event))

        except StatusError as e:
            redis_client.lpush('retry_blacklist', json.dumps(message._asdict()))
            logger.error('Timeout for bounty id (added to blacklist_retry): {}'.format(
                message.bounty_id))
            raise e
            # if e.original.response.status_code == 504:
            #     redis_client.lpush('retry_blacklist', json.dumps(message._asdict()))
                # logger.error('Timeout for bounty id (added to blacklist_retry): {}'.format(
                #     message.bounty_id))
            # raise e
