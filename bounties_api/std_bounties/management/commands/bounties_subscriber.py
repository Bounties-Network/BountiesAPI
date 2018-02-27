import os
from django.core.management.base import BaseCommand
import boto3
import time
from django.core.cache import cache
from std_bounties.client import BountyClient
from django.conf import settings
from slackclient import SlackClient
import logging

logger = logging.getLogger('django')

# redis transaction gets frozen for 5 days
cache_period = 432000

class Command(BaseCommand):
    help = 'Listen for contract events'

    def handle(self, *args, **options):
        try:
            bounty_client = BountyClient()
            sqs = boto3.client('sqs', region_name='us-east-1')
            sc = SlackClient(settings.SLACK_TOKEN)

            while True:
                # poll by the second
                time.sleep(1)

                response = sqs.receive_message(
                    QueueUrl = settings.QUEUE_URL,
                    AttributeNames=['MessageDeduplicationId'],
                    MessageAttributeNames=['All'],

                )

                messages = response.get('Messages')

                if not messages:
                    continue

                message = messages[0]
                receipt_handle = message['ReceiptHandle']
                transaction_id = message['Attributes']['MessageDeduplicationId']
                message_attributes = message['MessageAttributes']

                event = message_attributes['Event']['StringValue']
                bounty_id = int(message_attributes['BountyId']['StringValue'])
                fulfillment_id = int(message_attributes['FulfillmentId']['StringValue'])

                if event == 'BountyIssued':
                    bounty_client.issue_bounty(bounty_id)

                if event == 'BountyActivated':
                    bounty_client.activate_bounty(bounty_id)

                if event == 'BountyFulfilled':
                    bounty_client.fulfill_bounty(bounty_id, fulfillment_id)

                if event == 'FulfillmentUpdated':
                    bounty_client.update_fulfillment(bounty_id, fulfillment_id)

                if event == 'BountyKilled':
                    bounty_client.kill_bounty(bounty_id)

                if event == 'ContributionAdded':
                    bounty_client.add_contribution(bounty_id)

                if event == 'DeadlineExtended':
                    bounty_client.extend_deadline(bounty_id)

                if event == 'BountyChanged':
                    bounty_client.change_bounty(bounty_id)

                if event == 'IssuerTransferred':
                    bounty_client.transfer_issuer(bounty_id)

                if event == 'PayoutIncreased':
                    bounty_client.increase_payout(bounty_id)

                sc.api_call('chat.postMessage', channel='#bounty_notifs',
                    text='Event {} passed for bounty {}'.format(event, str(bounty_id))
                )
                cache.set(transaction_id, True, cache_period)
                sqs.delete_message(
                    QueueUrl=settings.QUEUE_URL,
                    ReceiptHandle=receipt_handle,
                )
        except Exception as e:
            # goes to rollbar
            logger.error(e)
            raise e


