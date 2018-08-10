import json
import time
from datetime import datetime

class Message:
    receipt_handle = ''
    event = ''
    bounty_id = -1
    fulfillment_id = -1
    message_deduplication_id = ''
    transaction_from = ''
    transaction_hash = ''
    event_timestamp = -1
    event_date = ''
    contract_method_inputs = {}

    @classmethod
    def message_from_event(event):
        if not message:
            return False

        message_attributes = message['MessageAttributes']

        return Message(
            receipt_handle=message['ReceiptHandle'],
            event=message_attributes['Event']['StringValue'],
            bounty_id=int(message_attributes['BountyId']['StringValue']),
            fulfillment_id=int(message_attributes['FulfillmentId']['StringValue']),
            message_deduplication_id=message_attributes['MessageDeduplicationId']['StringValue'],
            transaction_from=message_attributes['TransactionFrom']['StringValue'],
            transaction_hash=message_attributes['TransactionHash']['StringValue'],
            event_timestamp=message_attributes['TimeStamp']['StringValue'],
            event_date=datetime.fromtimestamp(int(event_timestamp)),
            contract_method_inputs=json.loads(
                message_attributes['ContractMethodInputs']['StringValue'])
        )

    def __init__(self, *args, **kwargs):
        if (kwargs):
            self.__dict__.update(kwargs)
        elif (args):
            self.__dict__.update(json.loads(*args))
    
    def __str__(self):
        modifiedSelf = self.__dict__
        modifiedSelf.event_date = str(modifiedSelf.event_date)
        return json.dumps(modifiedSelf)
