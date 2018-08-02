import json
import time
import datetime
from collections import namedtuple


Message = namedtuple('Message', (
    'receipt_handle,'
    'event,'
    'bounty_id,'
    'fulfillment_id,'
    'message_deduplication_id,'
    'transaction_from,'
    'transaction_hash,'
    'event_timestamp,'
    'event_date,'
    'contract_method_inputs'))
  

x = Message(
  receipt_handle='434806a2-d8db-45e8-8b46-8f9b41fb65d3#c9adaa49-8d45-420a-81ab-1a7071c389df',
  event='BountyIssued',
  bounty_id=42,
  fulfillment_id=12345,
  message_deduplication_id='0xaabed95c156cc8cc0f0e65d9d9f8851b400bdb6665266d367a5e0972a3bff927BountyIssued',
  transaction_from='0xbfDb50Dc66C8Df9fd9688D8fe5A0C34126427645',
  transaction_hash='0xaabed95c156cc8cc0f0e65d9d9f8851b400bdb6665266d367a5e0972a3bff927',
  event_timestamp='1513709342',
  event_date='2017-12-19 13:49:02',
  contract_method_inputs={'bountyId': '38', 'data': 'Qma7vipDNoPYph96ZfNasTD7jczhtJRM8TRL9RUDkzLyNB'},
)

#   'MessageId': '434806a2-d8db-45e8-8b46-8f9b41fb65d3'
# 'ReceiptHandle': '434806a2-d8db-45e8-8b46-8f9b41fb65d3#c9adaa49-8d45-420a-81ab-1a7071c389df'
# 'MD5OfBody': '0c649b864f2237f67326bbb805f5d951'
# 'Body': 'Event Subscription'
# 'MD5OfMessageAttributes': 'abab189d8ad0de339b91650df805d9c4'
# 'MessageAttributes': 
# 'TimeStamp': 
# 'StringValue': '1513709342'

# 'Event': 
# 'StringValue': 'BountyIssued'

# 'FulfillmentId': 
# 'StringValue': '-1'

# 'MessageDeduplicationId': 
# 'StringValue': '0xaabed95c156cc8cc0f0e65d9d9f8851b400bdb6665266d367a5e0972a3bff927BountyIssued'

# 'BountyId': 
# 'StringValue': '0'

# 'ContractMethodInputs': 
# 'StringValue': '{"issuer":"0xbfdb50dc66c8df9fd9688d8fe5a0c34126427645"
# "deadline":"1544573520"
# "data":"QmNk3CfMScMut3kcFKP7DMCV1y1ZF99D8N3hNZ1bmGqj2T"
# "fulfillmentAmount":"10000000000000000000"
# "arbiter":"0x0000000000000000000000000000000000000000"
# "paysTokens":false,"tokenContract":"0x0000000000000000000000000000000000000000"
# "value":"10000000000000000000"}'

# 'TransactionHash': 
# 'StringValue': '0xaabed95c156cc8cc0f0e65d9d9f8851b400bdb6665266d367a5e0972a3bff927'

# 'TransactionFrom': 
# 'StringValue': '0xbfDb50Dc66C8Df9fd9688D8fe5A0C34126427645'


def message_to_string(self, message):
    if not message:
        return False
    
    message.event_date = str(message.event_date)
    return json.dumps(message._asdict())
    
    # return Message(
    #     receipt_handle=message.receipt_handle,
    #     event=message.event,
    #     bounty_id=message.bounty_id,
    #     fulfillment_id=message.fulfillment_id,
    #     message_deduplication_id=message.message_deduplication_id,
    #     transaction_from=message.transaction_from,
    #     transaction_hash=message.transaction_hash,
    #     event_timestamp=message.event_timestamp,
    #     event_date=str(message.event_date),
    #     contract_method_inputs=json.dumps(message.contract_method_inputs)
    # )

def string_to_message(self, message):
    if not message:
        return False

    return Message(
        receipt_handle=message['receipt_handle'],
        event=message['event'],
        bounty_id=int(message['bounty_id']),
        fulfillment_id=int(message['fulfillment_id']),
        message_deduplication_id=message['message_deduplication_id'],
        transaction_from=message['transaction_from'],
        transaction_hash=message['transaction_hash'],
        event_timestamp=message['event_timestamp'],
        event_date=datetime.datetime.fromisoformat(message['event_date']),
        contract_method_inputs=json.loads(message['contract_method_inputs'])
    )

def unwrap_message(self, message):
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
        event_date=datetime.datetime.fromtimestamp(int(event_timestamp)),
        contract_method_inputs=json.loads(
            message_attributes['ContractMethodInputs']['StringValue'])
    )