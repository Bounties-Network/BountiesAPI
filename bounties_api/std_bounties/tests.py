import json
import unittest
from datetime import datetime
from decimal import Decimal

from std_bounties.bounty_client import BountyClient
from std_bounties.client_helpers import calculate_token_quantity, \
    calculate_usd_price, get_token_pricing, map_bounty_data, \
    map_fulfillment_data
from std_bounties.constants import ACTIVE_STAGE, DRAFT_STAGE, COMPLETED_STAGE
from std_bounties.models import Bounty, Token, Fulfillment
from std_bounties.message import Message


class TestCalculationHelpers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.eth_token = Token(
            normalized_name='ethereum',
            name='Ethereum',
            symbol='ETH',
            price_usd='600')
        cls.eth_token.save()

    def test_calculate_token_quantity(self):
        value = '100000'
        decimals = 3
        expected = Decimal('100')

        result = calculate_token_quantity(value, decimals)
        self.assertEqual(result, expected)

    def test_calculate_token_quantity_with_fraction(self):
        value = '100500'
        decimals = 3
        expected = Decimal('100.5')

        result = calculate_token_quantity(value, decimals)
        self.assertEqual(result, expected)

    def test_calculate_token_quantity_just_fraction(self):
        value = '500'
        decimals = 3
        expected = Decimal('0.5')

        result = calculate_token_quantity(value, decimals)
        self.assertEqual(result, expected)

    def test_calculate_usd_price_correctly_quantizes(self):
        value = '123456789123456789'
        decimals = 9
        usd_rate = 1
        expected = Decimal('123456789.12345679')

        result = calculate_usd_price(value, decimals, usd_rate)
        self.assertEqual(result, expected)

    def test_calculate_usd_price_correctly_applies_usd_rate(self):
        value = '100000'
        decimals = 2
        usd_rate = 2
        expected = Decimal('2000')

        result = calculate_usd_price(value, decimals, usd_rate)
        self.assertEqual(result, expected)

    def test_get_token_pricing_for_nonexistent_token(self):
        token_symbol = 'NEX'
        token_decimals = 5
        value = 100
        expected_token_model = None
        expected_usd_price = 0

        usd_price, token_model = get_token_pricing(token_symbol,
                                                   token_decimals, value)
        self.assertEqual(token_model, expected_token_model)
        self.assertEqual(usd_price, expected_usd_price)

    def test_get_token_pricing_for_existing_token(self):
        token_symbol = self.eth_token.symbol
        token_decimals = 5
        value = 100
        expected_usd_price = Decimal('0.6')

        usd_price, token_model = get_token_pricing(token_symbol,
                                                   token_decimals, value)
        self.assertEqual(token_model, self.eth_token)
        self.assertEqual(usd_price, expected_usd_price)


class TestMapBountyData(unittest.TestCase):

    def get_ipfs_data(self):
        issuer = {
            'name': 'issuer name',
            'email': 'issuer@issuer.com',
            'githubUsername': 'issuerGithub',
            'address': '0x32Be343B94f860124dC4fEe278FDCBD38C102D88'
        }
        meta = {
            'platform': 'gitcoin',
            'schemaVersion': '0.1',
            'schemaName': 'gitcoinSchema'
        }
        payload = {
            'title': 'BountyTitle',
            'description': 'Description of bounty',
            'issuer': issuer,
            'funders': [
                issuer,
            ],
            'categories': ['python'],
            'created': '1527881995',
            'tokenSymbol': 'ETH',
            'tokenAddress': '0x0',
            'sourceFileName': 'sourceFile',
            'sourceFileHash': 'QmRAQB6YaCyidP37UdDnjFY5vQuiBrcqdyoW1CuDgwxkD4',
            'webReferenceURL': 'some-url.com/with-reference',
            'sourceDirectoryHash':
            'QmXExS4BMc1YrH6iWERyryFcDWkvobxryXSwECLrcd7Y1H'
        }

        return {'payload': payload, 'meta': meta}

    def get_ipfs_data_as_json(self):
        return json.dumps(self.get_ipfs_data())

    def setUp(self):
        self.patcher = unittest.mock.patch('std_bounties.client_helpers.ipfs')
        self.mocked_ipfs = self.patcher.start()
        self.mocked_ipfs.cat.return_value = self.get_ipfs_data_as_json()
        self.addCleanup(self.patcher.stop)

    def test_map_bounty_data(self):
        data_hash = 'QmTDMoVqvyBkNMRhzvukTDznntByUNDwyNdSfV8dZ3VKRC'
        bounty_id = 1
        ipfs_data = self.get_ipfs_data()
        ipfs_data_as_json = self.get_ipfs_data_as_json()

        result = map_bounty_data(data_hash, bounty_id)
        self.assertEqual(result['issuer_name'],
                         ipfs_data['payload']['issuer']['name'])
        self.assertEqual(result['issuer_email'],
                         ipfs_data['payload']['issuer']['email'])
        self.assertEqual(result['issuer_githubUsername'],
                         ipfs_data['payload']['issuer']['githubUsername'])
        self.assertEqual(result['issuer_address'],
                         ipfs_data['payload']['issuer']['address'])
        self.assertEqual(result['data_issuer'], ipfs_data['payload']['issuer'])
        self.assertEqual(result['data'], data_hash)
        self.assertEqual(result['data_json'], ipfs_data_as_json)
        self.assertEqual(result['data_categories'],
                         ipfs_data['payload']['categories'])
        self.assertEqual(result['platform'], ipfs_data['meta']['platform'])
        self.assertEqual(result['schemaName'], ipfs_data['meta']['schemaName'])
        self.assertEqual(result['schemaVersion'],
                         ipfs_data['meta']['schemaVersion'])
        self.assertEqual(result['description'],
                         ipfs_data['payload']['description'])
        self.assertEqual(result['title'], ipfs_data['payload']['title'])
        self.assertEqual(result['sourceFileName'],
                         ipfs_data['payload']['sourceFileName'])
        self.assertEqual(result['sourceFileHash'],
                         ipfs_data['payload']['sourceFileHash'])
        self.assertEqual(result['sourceDirectoryHash'],
                         ipfs_data['payload']['sourceDirectoryHash'])


class TestMapFullfilmentData(unittest.TestCase):

    def get_ipfs_data(self):
        fulfiller = {
            'name': 'fulfiller name',
            'email': 'fulfiller@fulfiller.com',
            'githubUsername': 'fulfillerGithub',
            'address': '0x32Be343B94f860124dC4fEe278FDCBD38C102D89'
        }
        meta = {
            'platform': 'gitcoin',
            'schemaVersion': '0.1',
            'schemaName': 'gitcoinSchema'
        }
        payload = {
            'description': 'Description of fulfillment',
            'fulfiller': fulfiller,
            'sourceFileName': 'sourceFile',
            'sourceFileHash': 'QmRAQB6YaCyidP37UdDnjFY5vQuiBrcqdyoW1CuDgwxkD4',
            'sourceDirectoryHash':
            'QmXExS4BMc1YrH6iWERyryFcDWkvobxryXSwECLrcd7Y1H'
        }

        return {'payload': payload, 'meta': meta}

    def get_ipfs_data_as_json(self):
        return json.dumps(self.get_ipfs_data())

    def setUp(self):
        self.patcher = unittest.mock.patch('std_bounties.client_helpers.ipfs')
        self.mocked_ipfs = self.patcher.start()
        self.mocked_ipfs.cat.return_value = self.get_ipfs_data_as_json()
        self.addCleanup(self.patcher.stop)

    def test_map_fullfilment_data(self):
        data_hash = 'QmTDMoVqvyBkNMRhzvukTDznntByUNDwyNdSfV8dZ3VKRC'
        bounty_id = 1
        fulfillment_id = 1
        ipfs_data = self.get_ipfs_data()
        ipfs_data_as_json = self.get_ipfs_data_as_json()

        result = map_fulfillment_data(data_hash, bounty_id, fulfillment_id)
        self.assertEqual(result['fulfiller_name'],
                         ipfs_data['payload']['fulfiller']['name'])
        self.assertEqual(result['fulfiller_email'],
                         ipfs_data['payload']['fulfiller']['email'])
        self.assertEqual(result['fulfiller_githubUsername'],
                         ipfs_data['payload']['fulfiller']['githubUsername'])
        self.assertEqual(result['fulfiller_address'],
                         ipfs_data['payload']['fulfiller']['address'])
        self.assertEqual(result['data_fulfiller'],
                         ipfs_data['payload']['fulfiller'])
        self.assertEqual(result['data'], data_hash)
        self.assertEqual(result['data_json'], ipfs_data_as_json)
        self.assertEqual(result['platform'], ipfs_data['meta']['platform'])
        self.assertEqual(result['schemaName'], ipfs_data['meta']['schemaName'])
        self.assertEqual(result['schemaVersion'],
                         ipfs_data['meta']['schemaVersion'])
        self.assertEqual(result['description'],
                         ipfs_data['payload']['description'])
        self.assertEqual(result['sourceFileName'],
                         ipfs_data['payload']['sourceFileName'])
        self.assertEqual(result['sourceFileHash'],
                         ipfs_data['payload']['sourceFileHash'])
        self.assertEqual(result['sourceDirectoryHash'],
                         ipfs_data['payload']['sourceDirectoryHash'])


class TestBountyClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = BountyClient()

    def test_issue_bounty(self):
        bounty_id = 25
        issuer = '0x4242424242424242424242424242424242424242'
        inputs = {
            'data': 'QmQjchBM6tjAvXzkDEpWgLUv9Ui4jwqtxsEzB6LxB2WqFL',
            'paysTokens': False,
            'tokenContract': '0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359',
            'fulfillmentAmount': 1,
            'issuer': issuer,
            'deadline': '1550529106',
        }
        issue_timestamp = '1517536922'
        issue_datetime = datetime.fromtimestamp(int(issue_timestamp))
        bounty = self.client.issue_bounty(
            bounty_id=bounty_id,
            inputs=inputs,
            event_timestamp=issue_timestamp)
        self.assertEqual(bounty.id, bounty_id)
        self.assertEqual(bounty.bounty_id, bounty_id)
        self.assertEqual(bounty.bounty_created, issue_datetime)
        self.assertEqual(bounty.bountyStage, DRAFT_STAGE)
        self.assertEqual(bounty.issuer, issuer)

    def test_activate_bounty(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_activate = Bounty(
            id=1,
            bounty_id=1,
            fulfillmentAmount=1,
            usd_price=1,
            deadline=deadline,
            paysTokens=True,
            created=created,
            bountyStage=DRAFT_STAGE)
        bounty_to_activate.save()
        bounty_to_activate_id = bounty_to_activate.id
        # Activate bounty
        activation_timestamp = '1517536922'
        bounty_to_activate = Bounty.objects.get(pk=bounty_to_activate_id)

        result = self.client.activate_bounty(
            bounty=bounty_to_activate,
            inputs={},
            event_timestamp=activation_timestamp)

        self.assertEqual(result.bountyStage, ACTIVE_STAGE)

        activated_bounty_from_db = Bounty.objects.get(
            pk=bounty_to_activate_id)
        self.assertEqual(result, activated_bounty_from_db)

    def test_fulfill_bounty(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_fulfill = Bounty(
            id=2,
            bounty_id=2,
            balance=1,
            fulfillmentAmount=1,
            usd_price=10,
            deadline=deadline,
            paysTokens=True,
            created=created,
            bountyStage=ACTIVE_STAGE)
        bounty_to_fulfill.save()
        bounty_to_fulfill_id = bounty_to_fulfill.id
        # Fulfill bounty
        bounty_to_fulfill = Bounty.objects.get(pk=bounty_to_fulfill_id)
        fulfillment_timestamp = '1517536922'
        fulfillment_datetime = datetime.fromtimestamp(int(fulfillment_timestamp))
        fulfillment_id = 10
        issuer = '0x4242424242424242424242424242424242424242'
        inputs = {
            'data': 'QmQjchBM6tjAvXzkDEpWgLUv9Ui4jwqtxsEzB6LxB2WqFL'
        }
        fulfillment = self.client.fulfill_bounty(
            bounty=bounty_to_fulfill,
            fulfillment_id=fulfillment_id,
            inputs=inputs,
            event_timestamp=fulfillment_timestamp,
            transaction_issuer=issuer)

        self.assertEqual(fulfillment.fulfillment_id, fulfillment_id)
        self.assertEqual(fulfillment.bounty.id, bounty_to_fulfill_id)
        self.assertEqual(fulfillment.accepted, False)
        self.assertEqual(fulfillment.fulfiller, issuer)
        self.assertEqual(fulfillment.fulfillment_created, fulfillment_datetime)

        # Try fulfill with duplicate id
        fulfillment = self.client.fulfill_bounty(
            bounty=bounty_to_fulfill,
            fulfillment_id=fulfillment_id,
            inputs=inputs,
            event_timestamp=fulfillment_timestamp,
            transaction_issuer=issuer)
        self.assertIsNone(fulfillment)

    def test_accept_fulfillment(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_fulfill = Bounty(
            id=3,
            bounty_id=3,
            balance=1,
            fulfillmentAmount=1,
            usd_price=10,
            deadline=deadline,
            paysTokens=True,
            created=created,
            bountyStage=ACTIVE_STAGE)
        bounty_to_fulfill.save()
        bounty_to_fulfill_id = bounty_to_fulfill.id
        # Create fulfillment
        fulfillment_to_accept = Fulfillment(
            fulfillment_id=1,
            fulfiller='0x4242424242424242424242424242424242424242',
            bounty=bounty_to_fulfill,
            accepted=True,
            created=created)
        fulfillment_to_accept.save()
        fulfillment_to_accept_id = fulfillment_to_accept.id
        # Accept fulfillment
        bounty_to_fulfill = Bounty.objects.get(pk=bounty_to_fulfill_id)
        fulfillment_timestamp = '1517536922'
        fulfillment_datetime = datetime.fromtimestamp(int(fulfillment_timestamp))
        fulfillment_to_accept = Fulfillment.objects.get(pk=fulfillment_to_accept_id)
        fulfillment = self.client.accept_fulfillment(
            bounty=bounty_to_fulfill,
            fulfillment_id=fulfillment_to_accept.fulfillment_id,
            event_timestamp=fulfillment_timestamp)
        self.assertEqual(fulfillment.bounty.bountyStage, COMPLETED_STAGE)
        self.assertEqual(fulfillment.accepted, True)
        self.assertEqual(fulfillment.accepted_date, fulfillment_datetime)
        self.assertEqual(bounty_to_fulfill.balance, 0)

    def test_kill_bounty(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_kill = Bounty(
            id=4,
            bounty_id=4,
            balance=1,
            fulfillmentAmount=1,
            usd_price=10,
            paysTokens=True,
            created=created,
            deadline=deadline,
            bountyStage=ACTIVE_STAGE)
        bounty_to_kill.save()
        bounty_to_kill_id = bounty_to_kill.id
        # Kill bounty
        bounty_to_kill = Bounty.objects.get(pk=bounty_to_kill_id)
        fulfillment_timestamp = '1517536922'
        bounty = self.client.kill_bounty(
            bounty=bounty_to_kill,
            event_timestamp=fulfillment_timestamp)
        self.assertEqual(bounty.bountyStage, COMPLETED_STAGE)

    def test_add_contribution(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_top_up = Bounty(
            id=5,
            bounty_id=5,
            balance=0,
            fulfillmentAmount=10,
            usd_price=10,
            paysTokens=True,
            created=created,
            deadline=deadline,
            bountyStage=COMPLETED_STAGE)
        bounty_to_top_up.save()
        bounty_to_top_up_id = bounty_to_top_up.id
        # Top up bounty with amount that is not enough to make it active
        bounty_to_top_up = Bounty.objects.get(pk=bounty_to_top_up_id)
        old_balance = bounty_to_top_up.balance
        inputs = {
            'value': 2
        }
        fulfillment_timestamp = '1517536922'
        bounty = self.client.add_contribution(
            bounty=bounty_to_top_up,
            inputs=inputs,
            event_timestamp=fulfillment_timestamp)
        new_balance = old_balance + inputs['value']
        self.assertEqual(bounty.bountyStage, COMPLETED_STAGE)
        self.assertEqual(bounty.balance, new_balance)
        # Top up bounty with amount enough to make it active
        bounty_to_top_up = Bounty.objects.get(pk=bounty_to_top_up_id)
        old_balance = bounty_to_top_up.balance
        inputs = {
            'value': 10
        }
        fulfillment_timestamp = '1517536922'
        bounty = self.client.add_contribution(
            bounty=bounty_to_top_up,
            inputs=inputs,
            event_timestamp=fulfillment_timestamp)
        new_balance = old_balance + inputs['value']
        self.assertEqual(bounty.bountyStage, ACTIVE_STAGE)
        self.assertEqual(bounty.balance, new_balance)
        # Top up bounty that is already active
        bounty_to_top_up = Bounty.objects.get(pk=bounty_to_top_up_id)
        old_balance = bounty_to_top_up.balance
        inputs = {
            'value': 10
        }
        fulfillment_timestamp = '1517536922'
        bounty = self.client.add_contribution(
            bounty=bounty_to_top_up,
            inputs=inputs,
            event_timestamp=fulfillment_timestamp)
        new_balance = old_balance + inputs['value']
        self.assertEqual(bounty.bountyStage, ACTIVE_STAGE)
        self.assertEqual(bounty.balance, new_balance)

    def test_extend_deadline(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_extend_deadline = Bounty(
            id=6,
            bounty_id=6,
            fulfillmentAmount=1,
            usd_price=1,
            deadline=deadline,
            paysTokens=True,
            created=created,
            bountyStage=ACTIVE_STAGE)
        bounty_to_extend_deadline.save()
        bounty_to_extend_deadline_id = bounty_to_extend_deadline.id
        # Extend bounty deadline
        event_timestamp = '1517536922'
        new_deadline_timestamp = '1818636922'
        inputs = {'newDeadline': new_deadline_timestamp}
        bounty_to_extend_deadline = Bounty.objects.get(pk=bounty_to_extend_deadline_id)

        result = self.client.extend_deadline(
            bounty=bounty_to_extend_deadline,
            inputs=inputs,
            event_timestamp=event_timestamp)

        self.assertEqual(result.bountyStage, ACTIVE_STAGE)
        self.assertEqual(result.deadline, datetime(2027, 8, 19, 0, 55, 22))

        bounty_to_extend_deadline_from_db = Bounty.objects.get(
            pk=bounty_to_extend_deadline_id)
        self.assertEqual(result, bounty_to_extend_deadline_from_db)

    def test_change_bounty(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_change = Bounty(
            id=7,
            bounty_id=7,
            balance=1,
            fulfillmentAmount=1,
            usd_price=10,
            paysTokens=True,
            created=created,
            deadline=deadline,
            bountyStage=ACTIVE_STAGE)
        bounty_to_change.save()
        bounty_to_change_id = bounty_to_change.id
        # Change bounty
        bounty_to_change = Bounty.objects.get(pk=bounty_to_change_id)
        inputs = {
            'data': 'QmQjchBM6tjAvXzkDEpWgLUv9Ui4jwqtxsEzB6LxB2WqFL',
            'newDeadline': '1517536923',
            'newFulfillmentAmount': 2,
            'newArbiter': '0x4444444444444444444422222222222222222222'
        }
        new_deadline = datetime.fromtimestamp(int(inputs['newDeadline']))
        result = self.client.change_bounty(
            bounty=bounty_to_change,
            inputs=inputs)
        self.assertEqual(result.deadline, new_deadline)
        self.assertEqual(result.fulfillmentAmount, inputs['newFulfillmentAmount'])
        self.assertEqual(result.arbiter, inputs['newArbiter'])

    def test_transfer_issuer(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_transfer_issuer = Bounty(
            id=8,
            bounty_id=8,
            fulfillmentAmount=1,
            paysTokens=True,
            created=created,
            deadline=deadline,
            issuer='0x4242424242424242424242424242424242424242')
        bounty_to_transfer_issuer.save()
        bounty_to_transfer_issuer_id = bounty_to_transfer_issuer.id
        # Transfer issuer
        bounty_to_transfer_issuer = Bounty.objects.get(pk=bounty_to_transfer_issuer_id)
        inputs = {
            'newIssuer': '0x4444444444444444444422222222222222222222'
        }
        result = self.client.transfer_issuer(
            bounty=bounty_to_transfer_issuer,
            inputs=inputs)
        self.assertEqual(result.issuer, inputs['newIssuer'])

    def test_increase_payout(self):
        # Create bounty
        created = datetime(2018, 1, 1, 1, 1, 1)
        deadline = datetime(2019, 1, 1, 1, 1, 1)
        bounty_to_increase_payout = Bounty(
            id=9,
            bounty_id=9,
            balance=10,
            paysTokens=True,
            created=created,
            deadline=deadline,
            fulfillmentAmount=5)
        bounty_to_increase_payout.save()
        bounty_to_increase_payout_id = bounty_to_increase_payout.id
        # Increase payout without changing balance
        bounty_to_increase_payout = Bounty.objects.get(pk=bounty_to_increase_payout_id)
        old_balance = bounty_to_increase_payout.balance
        inputs = {
            'newFulfillmentAmount': 10
        }
        result = self.client.increase_payout(
            bounty=bounty_to_increase_payout,
            inputs=inputs)
        self.assertEqual(result.balance, old_balance)
        self.assertEqual(result.fulfillmentAmount, inputs['newFulfillmentAmount'])
        # Increase payout and increase balance
        bounty_to_increase_payout = Bounty.objects.get(pk=bounty_to_increase_payout_id)
        old_balance = bounty_to_increase_payout.balance
        inputs = {
            'value': 20,
            'newFulfillmentAmount': 20
        }
        result = self.client.increase_payout(
            bounty=bounty_to_increase_payout,
            inputs=inputs)
        new_balance = old_balance + inputs['value']
        self.assertEqual(result.balance, new_balance)
        self.assertEqual(result.fulfillmentAmount, inputs['newFulfillmentAmount'])


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
