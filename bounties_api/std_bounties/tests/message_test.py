import unittest
from datetime import datetime
from std_bounties.message import Message


class TestEventMessage(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        # Default values in variables, dict and string formats
        self.receipt_handle = '434806a2-d8db-45e8-8b46-8f9b41fb65d3#c9adaa49-8d45-420a-81ab-1a7071c389df'
        self.event = 'BountyIssued'
        self.bounty_id = 42
        self.fulfillment_id = 12345
        self.message_deduplication_id = '0x44444444444444444444444444444444442222222222222222222222222222222BountyIssued'
        self.transaction_from = '0x4444444444444444444422222222222222222222'
        self.transaction_hash = '0x4444444444444444444444444444444442222222222222222222222222222222'
        self.event_timestamp = '1513709342'
        self.event_date = datetime(2017, 12, 19, 18, 49, 2)
        self.contract_method_inputs = {
            'issuer': '0x4242424242424242424242424242424242424242',
            'deadline': '1550529106',
            'data': 'QmQjchBM6tjAvXzkDEpWgLUv9Ui4jwqtxsEzB6LxB2WqFL',
            'fulfillmentAmount': '42000000000000000',
            'arbiter': '0x0000000000000000000000000000000000000000',
            'paysTokens': False,
            'tokenContract': '0x0000000000000000000000000000000000000000',
            'value': '42000000000000000'
        }

        self.dict_values = {
            'receipt_handle': self.receipt_handle,
            'event': self.event,
            'bounty_id': self.bounty_id,
            'fulfillment_id': self.fulfillment_id,
            'message_deduplication_id': self.message_deduplication_id,
            'transaction_from': self.transaction_from,
            'transaction_hash': self.transaction_hash,
            'event_timestamp': self.event_timestamp,
            'event_date': self.event_date,
            'contract_method_inputs': self.contract_method_inputs,
        }

        self.string_values = """\
{
    "receipt_handle": "434806a2-d8db-45e8-8b46-8f9b41fb65d3#c9adaa49-8d45-420a-81ab-1a7071c389df",
    "event": "BountyIssued",
    "bounty_id": 42,
    "fulfillment_id": 12345,
    "message_deduplication_id": "0x44444444444444444444444444444444442222222222222222222222222222222BountyIssued",
    "transaction_from": "0x4444444444444444444422222222222222222222",
    "transaction_hash": "0x4444444444444444444444444444444442222222222222222222222222222222",
    "event_timestamp": "1513709342",
    "event_date": "2017-12-19T18:49:02",
    "contract_method_inputs": {
        "issuer": "0x4242424242424242424242424242424242424242",
        "deadline": "1550529106",
        "data": "QmQjchBM6tjAvXzkDEpWgLUv9Ui4jwqtxsEzB6LxB2WqFL",
        "fulfillmentAmount": "42000000000000000",
        "arbiter": "0x0000000000000000000000000000000000000000",
        "paysTokens": false,
        "tokenContract": "0x0000000000000000000000000000000000000000",
        "value": "42000000000000000"
    }
}\
"""

        self.event_values = {
            'MessageId': 'f0eeaa92-09fd-4398-a299-c53bbcd42319',
            'ReceiptHandle': '434806a2-d8db-45e8-8b46-8f9b41fb65d3#c9adaa49-8d45-420a-81ab-1a7071c389df',
            'MD5OfBody': '0c649b864f2237f67326bbb805f5d951',
            'Body': 'Event Subscription',
            'MD5OfMessageAttributes': '681c37e007c07743c65d75b5b8741f88',
            'MessageAttributes': {
                'TimeStamp': {
                    'StringValue': '1513709342',
                    'DataType': 'Number'
                },
                'Event': {
                    'StringValue': 'BountyIssued',
                    'DataType': 'String'
                },
                'FulfillmentId': {
                    'StringValue': '12345',
                    'DataType': 'Number'
                },
                'MessageDeduplicationId': {
                    'StringValue': '0x44444444444444444444444444444444442222222222222222222222222222222BountyIssued',
                    'DataType': 'String'
                },
                'BountyId': {
                    'StringValue': '42',
                    'DataType': 'Number'
                },
                'ContractMethodInputs': {
                    'StringValue': '{"issuer": "0x4242424242424242424242424242424242424242", "deadline": "1550529106", "data": "QmQjchBM6tjAvXzkDEpWgLUv9Ui4jwqtxsEzB6LxB2WqFL", "fulfillmentAmount": "42000000000000000", "arbiter": "0x0000000000000000000000000000000000000000", "paysTokens": false, "tokenContract": "0x0000000000000000000000000000000000000000", "value": "42000000000000000"}',
                    'DataType': 'String'
                },
                'TransactionHash': {
                    'StringValue': '0x4444444444444444444444444444444442222222222222222222222222222222',
                    'DataType': 'String'
                },
                'TransactionFrom': {
                    'StringValue': '0x4444444444444444444422222222222222222222',
                    'DataType': 'String'
                }
            }
        }

    def test_from_kwargs(self):
        message = Message(
            receipt_handle=self.receipt_handle,
            event=self.event,
            bounty_id=self.bounty_id,
            fulfillment_id=self.fulfillment_id,
            message_deduplication_id=self.message_deduplication_id,
            transaction_from=self.transaction_from,
            transaction_hash=self.transaction_hash,
            event_timestamp=self.event_timestamp,
            event_date=self.event_date,
            contract_method_inputs=self.contract_method_inputs
        )
        self.assertDictEqual(self.dict_values, message.__dict__)

    def test_create_from_dict(self):
        message = Message.from_dict(self.dict_values)
        self.assertDictEqual(self.dict_values, message.__dict__)

    def test_create_from_string(self):
        message = Message.from_string(self.string_values)
        self.assertDictEqual(self.dict_values, message.__dict__)

    def test_string_conversion(self):
        message = Message.from_dict(self.dict_values)
        self.assertEqual(self.string_values, str(message))

    def test_message_from_event(self):
        message = Message.from_event(self.event_values)
        self.assertEqual(self.string_values, str(message))
