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
    def setUp(self):
        self.patcher = unittest.mock.patch('std_bounties.client_helpers.ipfs')
        self.mocked_ipfs = self.patcher.start()
        self.mocked_ipfs.cat.return_value = "{\"data\":\"blabla\"}"
        self.addCleanup(self.patcher.stop)

    def test_map_bounty_data(self):
        data_hash = 'QmTDMoVqvyBkNMRhzvukTDznntByUNDwyNdSfV8dZ3VKRC'
        bounty_id = 1

        result = map_bounty_data(data_hash, bounty_id)
        self.assertEqual(result, 'dasda')


class TestMapFullfilmentData(unittest.TestCase):
    def setUp(self):
        self.patcher = unittest.mock.patch('std_bounties.client_helpers.ipfs')
        self.mocked_ipfs = self.patcher.start()
        self.mocked_ipfs.cat.return_value = "{\"data\":\"blabla\"}"
        self.addCleanup(self.patcher.stop)

    def test_map_fullfilment_data(self):
        data_hash = 'QmTDMoVqvyBkNMRhzvukTDznntByUNDwyNdSfV8dZ3VKRC'
        bounty_id = 1
        fulfillment_id = 1

        result = map_fulfillment_data(data_hash, bounty_id, fulfillment_id)
        self.assertEqual(result, 'dasda')
