import os
import json
import time
from django.core.management.base import BaseCommand
from std_bounties.client import BountyClient
from django.conf import settings
from slackclient import SlackClient
from bounties.redis_client import redis_client
from bounties.sqs_client import sqs_client
import logging

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = 'Listen for contract events'

    def handle(self, *args, **options):
        try:
            bounty_client = BountyClient()
            sc = SlackClient(settings.SLACK_TOKEN)

            while True:
                # poll by the second
                if not settings.LOCAL:
                    time.sleep(1)

                response = sqs_client.receive_message(
                    QueueUrl=settings.QUEUE_URL,
                    AttributeNames=['MessageDeduplicationId'],
                    MessageAttributeNames=['All'],
                )

                messages = response.get('Messages')

                if not messages:
                    continue

                message = messages[0]
                receipt_handle = message['ReceiptHandle']
                message_attributes = message['MessageAttributes']

                event = message_attributes['Event']['StringValue']
                bounty_id = int(message_attributes['BountyId']['StringValue'])
                fulfillment_id = int(message_attributes['FulfillmentId']['StringValue'])
                message_deduplication_id =  message_attributes['MessageDeduplicationId']['StringValue']
                contract_method_inputs = json.loads(message_attributes['ContractMethodInputs']['StringValue']);

                if event == 'BountyIssued':
                    bounty_client.issue_bounty(bounty_id, contract_method_inputs)

                if event == 'BountyActivated':
                    bounty_client.activate_bounty(bounty_id, contract_method_inputs)

                if event == 'BountyFulfilled':
                    bounty_client.fulfill_bounty(bounty_id, fulfillment_id, contract_method_inputs)

                if event == 'FulfillmentUpdated':
                    bounty_client.update_fulfillment(bounty_id, fulfillment_id, contract_method_inputs)

                if event == 'FulfillmentAccepted':
                    bounty_client.accept_fulfillment(bounty_id, fulfillment_id)

                if event == 'BountyKilled':
                    bounty_client.kill_bounty(bounty_id)

                if event == 'ContributionAdded':
                    bounty_client.add_contribution(bounty_id, contract_method_inputs)

                if event == 'DeadlineExtended':
                    bounty_client.extend_deadline(bounty_id, contract_method_inputs)

                if event == 'BountyChanged':
                    bounty_client.change_bounty(bounty_id, contract_method_inputs)

                if event == 'IssuerTransferred':
                    bounty_client.transfer_issuer(bounty_id, contract_method_inputs)

                if event == 'PayoutIncreased':
                    bounty_client.increase_payout(bounty_id, contract_method_inputs)

                sc.api_call('chat.postMessage', channel='#bounty_notifs',
                    text='Event {} passed for bounty {}'.format(event, str(bounty_id))
                )
                redis_client.set(message_deduplication_id, True)
                sqs_client.delete_message(
                    QueueUrl=settings.QUEUE_URL,
                    ReceiptHandle=receipt_handle,
                )
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e


