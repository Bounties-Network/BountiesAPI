import os
import json
import time
from functools import partial

from django.core.management.base import BaseCommand
from std_bounties.client import BountyClient
from django.conf import settings
from slackclient import SlackClient
from bounties.redis_client import redis_client
from bounties.sqs_client import sqs_client
import logging

from std_bounties.client_helpers import apply_and_notify, bounty_url_for
from std_bounties.models import Bounty
from std_bounties.utils import narrower, wrapped_partial, merge

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
                          "{usd_price}, {deadline} {link}"
                    bounty = Bounty.objects.filter(bounty_id=bounty_id)
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    if not bounty.exists():
                        apply_and_notify(bounty_id,
                                         event='Bounty Issued',
                                         action=bounty_client.issue_bounty,
                                         inputs={'inputs': contract_method_inputs, 'event_timestamp': event_timestamp},
                                         fields=['title', 'bounty_id', 'tokenSymbol', 'tokenDecimals',
                                                 'fulfillmentAmount', 'usd_price', 'deadline'],
                                         msg=msg,
                                         slack_client=sc,
                                         before_formatter=[add_link]
                                         )

                if event == 'BountyActivated':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title} {bounty_id} {tokenSymbol} {usd_price} {link}"
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    apply_and_notify(bounty,
                                     event='Bounty Activated',
                                     action=bounty_client.activate_bounty,
                                     inputs={'inputs': contract_method_inputs},
                                     fields=['title', 'bounty_id', 'tokenSymbol', 'usd_price'],
                                     msg=msg,
                                     slack_client=sc,
                                     before_formatter=[add_link]
                                     )

                if event == 'BountyFulfilled':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}, {fulfillment_id},  {tokenSymbol} @ {tokenDecimals},"\
                          " {fulfillmentAmount}, {usd_price}, {deadline} {link}"
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    apply_and_notify(bounty,
                                     event='Bounty Fulfilled',
                                     action=bounty_client.fulfill_bounty,
                                     inputs={
                                         'fulfillment_id': fulfillment_id,
                                         'inputs': contract_method_inputs,
                                         'event_timestamp': event_timestamp,
                                         'transaction_issuer': transaction_from
                                     },
                                     fields=[('bounty__title', 'title'),
                                             ('bounty__bounty_id', 'bounty_id'),
                                             'fulfillment_id',
                                             ('bounty__tokenSymbol', 'tokenSymbol'),
                                             ('bounty__tokenDecimals', 'tokenDecimals'),
                                             ('bounty__fulfillmentAmount', 'fulfillmentAmount'),
                                             ('bounty__usd_price', 'usd_price'),
                                             ('bounty__deadline', 'deadline')],
                                     msg=msg,
                                     slack_client=sc,
                                     before_formatter=[add_link]
                                     )

                if event == 'FulfillmentUpdated':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}, {fulfillment_id} {link}"
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    apply_and_notify(bounty,
                                     event='Fulfillment Updated',
                                     action=bounty_client.update_fulfillment,
                                     inputs={'fulfillment_id': fulfillment_id, 'inputs': contract_method_inputs},
                                     fields=[('bounty__title', 'title'),
                                             ('bounty__bounty_id', 'bounty_id'),
                                             'fulfillment_id'
                                             ],
                                     msg=msg,
                                     slack_client=sc,
                                     before_formatter=[add_link]
                                     )

                if event == 'FulfillmentAccepted':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}, {fulfillment_id},  {tokenSymbol} @ {tokenDecimals},"\
                          " {fulfillmentAmount}, {usd_price}, {deadline} {link}"
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    apply_and_notify(bounty,
                                     event='Bounty Accepted',
                                     action=bounty_client.accept_fulfillment,
                                     inputs={'fulfillment_id': fulfillment_id},
                                     fields=[('bounty__title', 'title'),
                                             ('bounty__bounty_id', 'bounty_id'),
                                             'fulfillment_id',
                                             ('bounty__tokenSymbol', 'tokenSymbol'),
                                             ('bounty__tokenDecimals', 'tokenDecimals'),
                                             ('bounty__fulfillmentAmount', 'fulfillmentAmount'),
                                             ('bounty__usd_price', 'usd_price'),
                                             ('bounty__deadline', 'deadline')],
                                     msg=msg,
                                     slack_client=sc,
                                     before_formatter=[add_link]
                                     )

                if event == 'BountyKilled':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id} {link}"
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    apply_and_notify(bounty,
                                     event='Bounty Killed',
                                     action=bounty_client.kill_bounty,
                                     inputs={},
                                     fields=['title', 'bounty_id'],
                                     msg=msg,
                                     slack_client=sc,
                                     before_formatter=[add_link]
                                     )

                if event == 'ContributionAdded':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id}, {tokenDecimals}, {balance}, {usd_price}, {tokenDecimals},"\
                          "{old_balance} {link}"
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    apply_and_notify(bounty,
                                     event='Contribution Added',
                                     action=bounty_client.add_contribution,
                                     inputs={'inputs': contract_method_inputs},
                                     fields=['title',
                                             'bounty_id',
                                             'tokenDecimals',
                                             'balance',
                                             'usd_price',
                                             'tokenDecimals',
                                             'old_balance'
                                             ],
                                     msg=msg,
                                     slack_client=sc,
                                     before_formatter=[add_link]
                                     )

                if event == 'DeadlineExtended':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    previous_deadline = narrower(bounty, [('deadline', 'previous_deadline')])
                    msg = "{title}, {bounty_id}, {previous_deadline}, {deadline} {link}"
                    mix_previous_deadline = wrapped_partial(merge, source2=previous_deadline)
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    apply_and_notify(bounty,
                                     event='Deadline Extended',
                                     action=bounty_client.extend_deadline,
                                     inputs={'inputs': contract_method_inputs},
                                     fields=['title', 'bounty_id', 'deadline'],
                                     msg=msg,
                                     slack_client=sc,
                                     before_formatter=[mix_previous_deadline, add_link]
                                     )

                if event == 'BountyChanged':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id} {link}"
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    apply_and_notify(bounty,
                                     event='Bounty Changed',
                                     action=bounty_client.change_bounty,
                                     inputs={'inputs': contract_method_inputs},
                                     fields=['title', 'bounty_id'],
                                     msg=msg,
                                     slack_client=sc,
                                     before_formatter=[add_link]
                                     )

                if event == 'IssuerTransferred':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id} {link}"
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    apply_and_notify(bounty,
                                     event='Issuer Transferred',
                                     action=bounty_client.transfer_issuer,
                                     inputs={'inputs': contract_method_inputs},
                                     fields=['title', 'bounty_id'],
                                     msg=msg,
                                     slack_client=sc,
                                     before_formatter=[add_link]
                                     )

                if event == 'PayoutIncreased':
                    bounty = Bounty.objects.get(bounty_id=bounty_id)
                    msg = "{title}, {bounty_id} {link}"
                    add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})

                    apply_and_notify(bounty,
                                     event='Payout Increased',
                                     action=bounty_client.increase_payout,
                                     inputs={'inputs': contract_method_inputs},
                                     fields=['title',
                                             'bounty_id',
                                             ],
                                     msg=msg,
                                     slack_client=sc,
                                     before_formatter=[add_link]
                                     )

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
