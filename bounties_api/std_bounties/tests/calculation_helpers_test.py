import unittest
from decimal import Decimal
from std_bounties.models import Token
from std_bounties.client_helpers import calculate_token_quantity, calculate_usd_price, get_token_pricing


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
