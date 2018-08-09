import json
import time
import datetime

from django.core.management.base import BaseCommand

from std_bounties import master_client
from django.conf import settings
from bounties.redis_client import redis_client
from bounties.sqs_client import sqs_client
from std_bounties.models import Event
from . import message
import logging


logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Listen to SQS queue for contract events'

    def handle_message(self, message):
        try:
            # If someone uploads a data hash that is faulty, then we want to blacklist all events around that
            # bounty id. We manage this manually
            if redis_client.get('blacklist:' + str(message.bounty_id)):
                redis_client.set(message.message_deduplication_id, True)
                sqs_client.delete_message(
                    QueueUrl=settings.QUEUE_URL,
                    ReceiptHandle=message.receipt_handle,
                )
                return False

            event_defaults = {
                'bounty_id': message.bounty_id,
                'fulfillment_id': message.fulfillment_id if message.fulfillment_id != -1 else None,
                'transaction_from': message.transaction_from,
                'contract_inputs': message.contract_method_inputs,
                'event_date': message.event_date,
            }

            logger.info('get_or_create with defaults: {}'.format(event_defaults))

            Event.objects.get_or_create(
                event=event,
                transaction_hash=message.transaction_hash,
                defaults=event_defaults
            )

            logger.info(
                'attempting {}: for bounty id {}'.format(
                    event, str(message.bounty_id)))
            if event == 'BountyIssued':
                master_client.bounty_issued(message.bounty_id,
                                            event_date=message.event_date,
                                            inputs=message.contract_method_inputs,
                                            event_timestamp=message.event_timestamp)

            if event == 'BountyActivated':
                master_client.bounty_activated(message.bounty_id,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs,
                                                event_timestamp=message.event_timestamp)

            if event == 'BountyFulfilled':
                master_client.bounty_fulfilled(message.bounty_id,
                                                fulfillment_id=message.fulfillment_id,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs,
                                                event_timestamp=message.event_timestamp,
                                                transaction_issuer=message.transaction_from)

            if event == 'FulfillmentUpdated':
                master_client.fullfillment_updated(message.bounty_id,
                                                    event_date=message.event_date,
                                                    fulfillment_id=message.fulfillment_id,
                                                    inputs=message.contract_method_inputs)

            if event == 'FulfillmentAccepted':
                master_client.fulfillment_accepted(message.bounty_id,
                                                    event_date=message.event_date,
                                                    fulfillment_id=message.fulfillment_id,
                                                    event_timestamp=message.event_timestamp)

            if event == 'BountyKilled':
                master_client.bounty_killed(message.bounty_id,
                                            event_date=message.event_date,
                                            event_timestamp=message.event_timestamp)

            if event == 'ContributionAdded':
                master_client.contribution_added(message.bounty_id,
                                                    event_date=message.event_date,
                                                    inputs=message.contract_method_inputs,
                                                    event_timestamp=message.event_timestamp)

            if event == 'DeadlineExtended':
                master_client.deadline_extended(message.bounty_id,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs,
                                                event_timestamp=message.event_timestamp)

            if event == 'BountyChanged':
                master_client.bounty_changed(message.bounty_id,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs)

            if event == 'IssuerTransferred':
                master_client.issuer_transferred(message.bounty_id,
                                                transaction_from=message.transaction_from,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs)

            if event == 'PayoutIncreased':
                master_client.payout_increased(message.bounty_id,
                                                event_date=message.event_date,
                                                inputs=message.contract_method_inputs)

            logger.info(event)

            # This means the contract subscriber will never send this event
            # through to sqs again

            redis_client.set(message.message_deduplication_id, True)
            sqs_client.delete_message(
                QueueUrl=settings.QUEUE_URL,
                ReceiptHandle=message.receipt_handle,
            )

            return True



        except StatusError as e:
            redis_client.lpush('retry_blacklist', json.dumps(message._asdict()))
            logger.error('Timeout for bounty id (added to blacklist_retry): ' + message.bounty_id)
            raise e
            # if e.original.response.status_code == 504:
            #     redis_client.lpush('retry_blacklist', json.dumps(message._asdict()))
            #     logger.error('Timeout for bounty id (added to blacklist_retry): ' + message.bounty_id)
            # raise e

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

                message = Message(response.get('Messages'))

                retry_blacklist =- 1
                logger.info('done processing regular message, retry_blacklist is now: {}'.format(retry_blacklist))

                if retry_blacklist <= 0:
                    retry_blacklist = retry_blacklist_rate
                    logger.info('retry_blacklist reset to: {}'.format(retry_blacklist))
                    retry = redis_client.lrange('retry_blacklist', 0, -1)
                    for blacklisted in retry:
                        message = redis_client.get(blacklisted)
                        if message:
                            if self.handle_message(message):
                                redis_client.lrem('retry_blacklist', 0, blacklisted)
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
