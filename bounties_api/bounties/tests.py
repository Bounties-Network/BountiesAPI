import unittest

from bounties.utils import bounty_url_for


class TestBountyUrlFor(unittest.TestCase):

    bounty_id = 1
    colorado_platform = 'hiring'
    consensys_platform = 'berlin'

    def test_default_platform(self):
        expected = 'http://127.0.0.1/bounty/1'

        result = bounty_url_for(self.bounty_id)
        self.assertEqual(result, expected)

    def test_hiring_platform(self):
        expected = 'https://hiring.bounties.network/bounty/1'

        result = bounty_url_for(self.bounty_id, self.colorado_platform)
        self.assertEqual(result, expected)

    def test_berlin_platform(self):
        expected = 'https://berlin.bounties.network/bounty/1'

        result = bounty_url_for(self.bounty_id, self.consensys_platform)
        self.assertEqual(result, expected)
