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

from std_bounties.client_helpers import narrower, notify_slack, formatter, merge, pipe, wrapped_partial
from std_bounties.models import Bounty


logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Listen to SQS queue for contract events'

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
                fulfillment_id = int(
                    message_attributes['FulfillmentId']['StringValue'])
                message_deduplication_id = message_attributes['MessageDeduplicationId']['StringValue']
                transaction_from = message_attributes['TransactionFrom']['StringValue']
                event_timestamp = message_attributes['TimeStamp']['StringValue']
                contract_method_inputs = json.loads(
                    message_attributes['ContractMethodInputs']['StringValue'])

                # If someone uploads a data hash that is faulty, then we want to blacklist all events around that
                # bounty id. We manage this manually
                if redis_client.get('blacklist:' + str(bounty_id)):
                    redis_client.set(message_deduplication_id, True)
                    sqs_client.delete_message(
                        QueueUrl=settings.QUEUE_URL,
                        ReceiptHandle=receipt_handle,
                    )
                    continue

                logger.info(
                    'attempting {}: for bounty id {}'.format(
                        event, str(bounty_id)))
                if event == 'BountyIssued':
                    msg = "{title}, {bounty_id}, {tokenSymbol} @ {tokenDecimals}, {fulfillmentAmount}, "\
                          "{usd_price}, {deadline}"
                    bounty = Bounty.objects.filter(bounty_id=bounty_id)

                    if not bounty.exists():
                        pipe(bounty_id, [
                            wrapped_partial(bounty_client.issue_bounty,
                                            inputs=contract_method_inputs,
                                            event_timestamp=event_timestamp),
                            wrapped_partial(narrower,
                                            fields=['title', 'bounty_id', 'tokenSymbol', 'tokenDecimals',
                                                    'fulfillmentAmount', 'usd_price', 'deadline']),
                            wrapped_partial(formatter, msg),
                            wrapped_partial(notify_slack,
                                            sc,
                                            settings.NOTIFICATIONS_SLACK_CHANNEL,
                                            'Bounty Issued')
                        ])

                if event == 'BountyActivated':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title} {bounty_id} {tokenSymbol} {usd_price}"

                    pipe(bounty, [
                        wrapped_partial(bounty_client.activate_bounty, inputs=contract_method_inputs),
                        wrapped_partial(narrower, fields=['title', 'bounty_id', 'tokenSymbol', 'usd_price']),
                        wrapped_partial(formatter, msg),
                        wrapped_partial(notify_slack,
                                        sc,
                                        settings.NOTIFICATIONS_SLACK_CHANNEL,
                                        'Bounty Activated')
                    ])

                if event == 'BountyFulfilled':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}, {fulfillment_id},  {tokenSymbol} @ {tokenDecimals},"\
                          " {fulfillmentAmount}, {usd_price}, {deadline}"

                    pipe(bounty, [
                        wrapped_partial(bounty_client.fulfill_bounty,
                                        fulfillment_id=fulfillment_id,
                                        inputs=contract_method_inputs,
                                        event_timestamp=event_timestamp,
                                        transaction_issuer=transaction_from),
                        wrapped_partial(narrower,
                                        fields=[('bounty__title', 'title'),
                                                ('bounty__bounty_id', 'bounty_id'),
                                                'fulfillment_id',
                                                ('bounty__tokenSymbol', 'tokenSymbol'),
                                                ('bounty__tokenDecimals', 'tokenDecimals'),
                                                ('bounty__fulfillmentAmount', 'fulfillmentAmount'),
                                                ('bounty__usd_price', 'usd_price'),
                                                ('bounty__deadline', 'deadline')]),
                        wrapped_partial(formatter, msg),
                        wrapped_partial(notify_slack,
                                        sc,
                                        settings.NOTIFICATIONS_SLACK_CHANNEL,
                                        'Bounty Fullfilled')
                    ])

                if event == 'FulfillmentUpdated':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}, {fulfillment_id}"

                    pipe(bounty, [
                        wrapped_partial(bounty_client.update_fulfillment,
                                        fulfillment_id=fulfillment_id,
                                        inputs=contract_method_inputs),
                        wrapped_partial(narrower,
                                        fields=[('bounty__title', 'title'),
                                                ('bounty__bounty_id', 'bounty_id'),
                                                'fulfillment_id'
                                                ]),
                        wrapped_partial(formatter, msg),
                        wrapped_partial(notify_slack,
                                        sc,
                                        settings.NOTIFICATIONS_SLACK_CHANNEL,
                                        'Fulfillment Updated')
                    ])

                if event == 'FulfillmentAccepted':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}, {fulfillment_id},  {tokenSymbol} @ {tokenDecimals},"\
                          " {fulfillmentAmount}, {usd_price}, {deadline}"

                    pipe(bounty, [
                        wrapped_partial(bounty_client.accept_fulfillment, fulfillment_id=fulfillment_id),
                        wrapped_partial(narrower,
                                        fields=[('bounty__title', 'title'),
                                                ('bounty__bounty_id', 'bounty_id'),
                                                'fulfillment_id',
                                                ('bounty__tokenSymbol', 'tokenSymbol'),
                                                ('bounty__tokenDecimals', 'tokenDecimals'),
                                                ('bounty__fulfillmentAmount', 'fulfillmentAmount'),
                                                ('bounty__usd_price', 'usd_price'),
                                                ('bounty__deadline', 'deadline')]),
                        wrapped_partial(formatter, msg),
                        wrapped_partial(notify_slack,
                                        sc,
                                        settings.NOTIFICATIONS_SLACK_CHANNEL,
                                        'Bounty Accepted')
                    ])

                if event == 'BountyKilled':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}"

                    pipe(bounty, [
                        bounty_client.kill_bounty,
                        wrapped_partial(narrower,
                                        fields=['title',
                                                'bounty_id'
                                                ]
                                        ),
                        wrapped_partial(formatter, msg),
                        wrapped_partial(notify_slack,
                                        sc,
                                        settings.NOTIFICATIONS_SLACK_CHANNEL,
                                        'Bounty Killed')
                    ])

                if event == 'ContributionAdded':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}, {tokenDecimals}, {balance}, {usd_price}, {tokenDecimals},"\
                          "{old_balance}"

                    pipe(bounty, [
                        wrapped_partial(bounty_client.add_contribution, inputs=contract_method_inputs),
                        wrapped_partial(narrower,
                                        fields=['title',
                                                'bounty_id',
                                                'tokenDecimals',
                                                'balance',
                                                'usd_price',
                                                'tokenDecimals',
                                                'old_balance'
                                                ]
                                        ),
                        wrapped_partial(formatter, msg),
                        wrapped_partial(notify_slack,
                                        sc,
                                        settings.NOTIFICATIONS_SLACK_CHANNEL,
                                        'Contribution Added')
                    ])

                if event == 'DeadlineExtended':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    previous_deadline = narrower(bounty, [('deadline', 'previous_deadline')])
                    msg = "{title}, {bounty_id}, {previous_deadline}, {deadline}"

                    pipe(bounty, [
                        wrapped_partial(bounty_client.extend_deadline, inputs=contract_method_inputs),
                        wrapped_partial(narrower,
                                        fields=['title',
                                                'bounty_id',
                                                'deadline'
                                                ]),
                        wrapped_partial(merge, source2=previous_deadline),
                        wrapped_partial(formatter, msg),
                        wrapped_partial(notify_slack,
                                        sc,
                                        settings.NOTIFICATIONS_SLACK_CHANNEL,
                                        'Deadline Extended')
                    ])

                if event == 'BountyChanged':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}"

                    pipe(bounty, [
                        wrapped_partial(bounty_client.change_bounty, inputs=contract_method_inputs),
                        wrapped_partial(narrower,
                                        fields=['title',
                                                'bounty_id',
                                                ]),
                        wrapped_partial(formatter, msg),
                        wrapped_partial(notify_slack,
                                        sc,
                                        settings.NOTIFICATIONS_SLACK_CHANNEL,
                                        'Bounty Changed')
                    ])

                if event == 'IssuerTransferred':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}"

                    pipe(bounty, [
                        wrapped_partial(bounty_client.transfer_issuer, inputs=contract_method_inputs),
                        wrapped_partial(narrower,
                                        fields=['title',
                                                'bounty_id',
                                                ]),
                        wrapped_partial(formatter, msg),
                        wrapped_partial(notify_slack,
                                        sc,
                                        settings.NOTIFICATIONS_SLACK_CHANNEL,
                                        'Issuer Transferred')
                    ])

                if event == 'PayoutIncreased':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}"

                    pipe(bounty, [
                        wrapped_partial(bounty_client.increase_payout, inputs=contract_method_inputs),
                        wrapped_partial(narrower,
                                        fields=['title',
                                                'bounty_id',
                                                ]),
                        wrapped_partial(formatter, msg),
                        wrapped_partial(notify_slack,
                                        sc,
                                        settings.NOTIFICATIONS_SLACK_CHANNEL,
                                        'Payout Increased')
                    ])

                logger.info(event)

                # This means the contract subscriber will never send this event
                # through to sqs again
                redis_client.set(message_deduplication_id, True)
                sqs_client.delete_message(
                    QueueUrl=settings.QUEUE_URL,
                    ReceiptHandle=receipt_handle,
                )
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
