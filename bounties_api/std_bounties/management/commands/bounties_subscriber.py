import json
import time
import datetime

from django.core.management.base import BaseCommand

from std_bounties import master_client
from django.conf import settings
from bounties.redis_client import redis_client
from bounties.sqs_client import sqs_client
from std_bounties.models import Event
import logging


logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Listen to SQS queue for contract events'

    def handle_message(self, message):
        receipt_handle = message['ReceiptHandle']
        message_attributes = message['MessageAttributes']

        event = message_attributes['Event']['StringValue']
        bounty_id = int(message_attributes['BountyId']['StringValue'])
        fulfillment_id = int(
            message_attributes['FulfillmentId']['StringValue'])
        message_deduplication_id = message_attributes['MessageDeduplicationId']['StringValue']
        transaction_from = message_attributes['TransactionFrom']['StringValue']
        transaction_hash = message_attributes['TransactionHash']['StringValue']
        event_timestamp = message_attributes['TimeStamp']['StringValue']
        contract_method_inputs = json.loads(
            message_attributes['ContractMethodInputs']['StringValue'])
        event_date = datetime.datetime.fromtimestamp(int(event_timestamp))

        # If someone uploads a data hash that is faulty, then we want to blacklist all events around that
        # bounty id. We manage this manually
        if redis_client.get('blacklist:' + str(bounty_id)):
            redis_client.set(message_deduplication_id, True)
            sqs_client.delete_message(
                QueueUrl=settings.QUEUE_URL,
                ReceiptHandle=receipt_handle,
            )
            return

        event_defaults = {
            'bounty_id': bounty_id,
            'fulfillment_id': fulfillment_id if fulfillment_id != -1 else None,
            'transaction_from': transaction_from,
            'contract_inputs': contract_method_inputs,
            'event_date': event_date,
        }

        logger.info('get_or_create with defaults: {}'.format(event_defaults))

        Event.objects.get_or_create(
            event=event,
            transaction_hash=transaction_hash,
            defaults=event_defaults
        )

        logger.info(
            'attempting {}: for bounty id {}'.format(
                event, str(bounty_id)))
        if event == 'BountyIssued':
            master_client.bounty_issued(bounty_id,
                                        event_date=event_date,
                                        inputs=contract_method_inputs,
                                        event_timestamp=event_timestamp)

        if event == 'BountyActivated':
            master_client.bounty_activated(bounty_id,
                                            event_date=event_date,
                                            inputs=contract_method_inputs,
                                            event_timestamp=event_timestamp)

        if event == 'BountyFulfilled':
            master_client.bounty_fulfilled(bounty_id,
                                            fulfillment_id=fulfillment_id,
                                            event_date=event_date,
                                            inputs=contract_method_inputs,
                                            event_timestamp=event_timestamp,
                                            transaction_issuer=transaction_from)

        if event == 'FulfillmentUpdated':
            master_client.fullfillment_updated(bounty_id,
                                                event_date=event_date,
                                                fulfillment_id=fulfillment_id,
                                                inputs=contract_method_inputs)

        if event == 'FulfillmentAccepted':
            master_client.fulfillment_accepted(bounty_id,
                                                event_date=event_date,
                                                fulfillment_id=fulfillment_id,
                                                event_timestamp=event_timestamp)

        if event == 'BountyKilled':
            master_client.bounty_killed(bounty_id,
                                        event_date=event_date,
                                        event_timestamp=event_timestamp)

        if event == 'ContributionAdded':
            master_client.contribution_added(bounty_id,
                                                event_date=event_date,
                                                inputs=contract_method_inputs,
                                                event_timestamp=event_timestamp)

        if event == 'DeadlineExtended':
            master_client.deadline_extended(bounty_id,
                                            event_date=event_date,
                                            inputs=contract_method_inputs,
                                            event_timestamp=event_timestamp)

        if event == 'BountyChanged':
            master_client.bounty_changed(bounty_id,
                                            event_date=event_date,
                                            inputs=contract_method_inputs)

        if event == 'IssuerTransferred':
            master_client.issuer_transferred(bounty_id,
                                            transaction_from=transaction_from,
                                            event_date=event_date,
                                            inputs=contract_method_inputs)

        if event == 'PayoutIncreased':
            master_client.payout_increased(bounty_id,
                                            event_date=event_date,
                                            inputs=contract_method_inputs)

        logger.info(event)

        # This means the contract subscriber will never send this event
        # through to sqs again

        redis_client.set(message_deduplication_id, True)
        sqs_client.delete_message(
            QueueUrl=settings.QUEUE_URL,
            ReceiptHandle=receipt_handle,
        )

        return True

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
                )

                messages = response.get('Messages')

                if not messages:
                    continue

                self.handle_message(messages[0])

                retry_blacklist =- 1
                logger.info('done processing regular message, retry_blacklist is now: {}'.format(retry_blacklist))

                if retry_blacklist <= 0:
                    retry_blacklist = retry_blacklist_rate
                    logger.info('retry_blacklist reset to: {}'.format(retry_blacklist))
                    retry = redis_client.lrange('retry_blacklist', 0, -1)
                    for blacklisted in retry:
                        message = redis_client.get(blacklisted)
                        if message:
                            self.handle_message(message)
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
