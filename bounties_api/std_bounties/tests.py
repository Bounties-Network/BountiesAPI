import json
import unittest
from decimal import Decimal

from std_bounties.client_helpers import (bounty_url_for,
                                         calculate_token_quantity,
                                         calculate_usd_price,
                                         get_token_pricing, map_bounty_data,
                                         map_fulfillment_data)
from std_bounties.models import Token


class TestBountyUrlFor(unittest.TestCase):

    bounty_id = 1
    colorado_platform = 'colorado'
    consensys_platform = 'consensys'

    def test_default_platform(self):
        expected = 'http://127.0.0.1/bounty/v1/1/'

        result = bounty_url_for(self.bounty_id)
        self.assertEqual(result, expected)

    def test_colorado_platform(self):
        expected = 'https://colorado.bounties.network/bounty/v1/1/'

        result = bounty_url_for(self.bounty_id, self.colorado_platform)
        self.assertEqual(result, expected)

    def test_consensys_platform(self):
        expected = 'https://consensys.bounties.network/bounty/v1/1/'

        result = bounty_url_for(self.bounty_id, self.consensys_platform)
        self.assertEqual(result, expected)


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
