import unittest

from bounties.utils import bounty_url_for


class TestBountyUrlFor(unittest.TestCase):

    bounty_id = 1
    colorado_platform = 'colorado'
    consensys_platform = 'consensys'

    def test_default_platform(self):
        expected = 'http://127.0.0.1/bounty/1'

        result = bounty_url_for(self.bounty_id)
        self.assertEqual(result, expected)

    def test_colorado_platform(self):
        expected = 'https://colorado.bounties.network/bounty/1'

        result = bounty_url_for(self.bounty_id, self.colorado_platform)
        self.assertEqual(result, expected)

    def test_consensys_platform(self):
        expected = 'https://consensys.bounties.network/bounty/1'

        result = bounty_url_for(self.bounty_id, self.consensys_platform)
        self.assertEqual(result, expected)
