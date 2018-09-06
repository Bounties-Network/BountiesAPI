import json
from datetime import datetime


def to_serializable(val):
    """JSON serializer for objects not serializable by default"""

    if isinstance(val, datetime):
        return val.isoformat()
    elif hasattr(val, '__dict__'):
        return val.__dict__

    return val


class Message:
    receipt_handle = ''
    event = ''
    bounty_id = -1
    fulfillment_id = -1
    message_deduplication_id = ''
    transaction_from = ''
    transaction_hash = ''
    event_timestamp = -1
    event_date = None
    contract_method_inputs = {}

    @staticmethod
    def from_event(event):
        if not event:
            raise ValueError('Can\'t create message without event')
        elif event.__class__ != dict:
            raise TypeError('Event argument was not a dict')

        message_attributes = event['MessageAttributes']
        event_timestamp = message_attributes['TimeStamp']['StringValue']

        return Message(
            receipt_handle=event['ReceiptHandle'],
            event=message_attributes['Event']['StringValue'],
            bounty_id=int(message_attributes['BountyId']['StringValue']),
            fulfillment_id=int(message_attributes[
                               'FulfillmentId']['StringValue']),
            message_deduplication_id=message_attributes[
                'MessageDeduplicationId']['StringValue'],
            transaction_from=message_attributes[
                'TransactionFrom']['StringValue'],
            transaction_hash=message_attributes[
                'TransactionHash']['StringValue'],
            event_timestamp=event_timestamp,
            event_date=datetime.fromtimestamp(int(event_timestamp)),
            contract_method_inputs=json.loads(
                message_attributes['ContractMethodInputs']['StringValue'])
        )

    @staticmethod
    def from_string(string):
        if not string:
            raise ValueError('Can\'t create message without string')
        elif string.__class__ != str:
            raise TypeError('Event argument was not a string')

        dictionary = json.loads(string)
        dictionary['event_date'] = datetime.strptime(
            dictionary['event_date'], '%Y-%m-%dT%H:%M:%S')
        return Message.from_dict(dictionary)

    @staticmethod
    def from_dict(dictionary):
        message = Message()
        message.__dict__.update(dictionary)
        return message

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.__dict__.update(kwargs)

    def __str__(self):
        return json.dumps(self.__dict__, indent=4, default=to_serializable)
