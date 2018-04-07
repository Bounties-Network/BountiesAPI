from __future__ import unicode_literals
import datetime
import json
import logging
from decimal import Decimal
from django.contrib.postgres.fields import JSONField
from django.db import transaction

from analytics.models import Event


logger = logging.getLogger('django')


class AnalyticsClient:
    def receive_message(self, message):
        message_attributes = message['MessageAttributes']

        event_name = message_attributes['Event']['StringValue']
        transaction_hash = message_attributes['TransactionHash']['StringValue']
        bounty_id = int(message_attributes['BountyId']['StringValue'])
        fulfillment_id = int(
            message_attributes['FulfillmentId']['StringValue'])
        # message_deduplication_id = message_attributes['MessageDeduplicationId']['StringValue']
        transaction_from = message_attributes['TransactionFrom']['StringValue']
        event_timestamp = int(message_attributes['TimeStamp']['StringValue'])
        contract_method_inputs = json.loads(
            message_attributes['ContractMethodInputs']['StringValue'])

        event = Event(
            event_name=event_name,
            transaction_hash=transaction_hash,
            bounty_id=bounty_id,
            fulfillment_id=fulfillment_id,
            transaction_from=transaction_from,
            event_timestamp=event_timestamp,
            contract_method_inputs=contract_method_inputs
        )

        try:
            event.save()
            return true
        except Exception as e:
            logger.error(e)
            return false
