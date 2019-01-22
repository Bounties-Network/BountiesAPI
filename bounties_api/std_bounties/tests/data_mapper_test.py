import json
import unittest
from std_bounties.client_helpers import map_bounty_data, map_fulfillment_data


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
        self.assertEqual(result['issuer_name'], ipfs_data['payload']['issuer']['name'])
        self.assertEqual(result['issuer_email'], ipfs_data['payload']['issuer']['email'])
        self.assertEqual(result['issuer_githubUsername'], ipfs_data['payload']['issuer']['githubUsername'])
        self.assertEqual(result['issuer_address'], ipfs_data['payload']['issuer']['address'])
        self.assertEqual(result['data_issuer'], ipfs_data['payload']['issuer'])
        self.assertEqual(result['data'], data_hash)
        self.assertEqual(result['data_json'], ipfs_data_as_json)
        self.assertEqual(result['data_categories'], ipfs_data['payload']['categories'])
        self.assertEqual(result['platform'], ipfs_data['meta']['platform'])
        self.assertEqual(result['schemaName'], ipfs_data['meta']['schemaName'])
        self.assertEqual(result['schemaVersion'], ipfs_data['meta']['schemaVersion'])
        self.assertEqual(result['description'], ipfs_data['payload']['description'])
        self.assertEqual(result['title'], ipfs_data['payload']['title'])
        self.assertEqual(result['sourceFileName'], ipfs_data['payload']['sourceFileName'])
        self.assertEqual(result['sourceFileHash'], ipfs_data['payload']['sourceFileHash'])
        self.assertEqual(result['sourceDirectoryHash'], ipfs_data['payload']['sourceDirectoryHash'])


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
        self.assertEqual(result['fulfiller_name'], ipfs_data['payload']['fulfiller']['name'])
        self.assertEqual(result['fulfiller_email'], ipfs_data['payload']['fulfiller']['email'])
        self.assertEqual(result['fulfiller_githubUsername'], ipfs_data['payload']['fulfiller']['githubUsername'])
        self.assertEqual(result['fulfiller_address'], ipfs_data['payload']['fulfiller']['address'])
        self.assertEqual(result['data_fulfiller'], ipfs_data['payload']['fulfiller'])
        self.assertEqual(result['data'], data_hash)
        self.assertEqual(result['data_json'], ipfs_data_as_json)
        self.assertEqual(result['platform'], ipfs_data['meta']['platform'])
        self.assertEqual(result['schemaName'], ipfs_data['meta']['schemaName'])
        self.assertEqual(result['schemaVersion'], ipfs_data['meta']['schemaVersion'])
        self.assertEqual(result['description'], ipfs_data['payload']['description'])
        self.assertEqual(result['sourceFileName'], ipfs_data['payload']['sourceFileName'])
        self.assertEqual(result['sourceFileHash'], ipfs_data['payload']['sourceFileHash'])
        self.assertEqual(result['sourceDirectoryHash'], ipfs_data['payload']['sourceDirectoryHash'])
