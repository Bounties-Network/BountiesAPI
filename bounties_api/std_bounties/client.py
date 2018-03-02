import json
import datetime
from collections import namedtuple
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from std_bounties.contract import data
from std_bounties.models import Bounty, Fulfillment
from std_bounties.serializers import BountySerializer, FulfillmentSerializer
import ipfsapi


web3 = Web3(HTTPProvider('https://mainnet.infura.io/'))
RawFulfillmentData = namedtuple('RawFulfillmentData', ['accepted', 'fulfiller', 'data'])
RawBountyData = namedtuple('RawBountyData', [
    'issuer', 'deadline', 'fulfillmentAmount', 'paysTokens', 'bountyStage', 'balance',
])
bounties_json = json.loads(data)
StandardBounties = web3.eth.contract(
    bounties_json['interfaces']['StandardBounties'],
    bounties_json['mainNet']['standardBountiesAddress']['v1'],
    ContractFactoryClass=ConciseContract
)
ipfs = ipfsapi.connect(host='https://ipfs.infura.io')

class BountyClient:

    def __init__(self):
        pass

    def issue_bounty(self, id):
        bounty = Bounty.objects.filter(bounty_id=id).exists()
        if bounty:
            return
        bounty_response = StandardBounties.getBounty(id)
        raw_bounty = RawBountyData(*bounty_response)._asdict()
        arbiter = StandardBounties.getBountyArbiter(id)
        data_hash = StandardBounties.getBountyData(id)
        data_JSON = ipfs.cat(data_hash)
        data = json.loads(data_JSON)
        if 'payload' in data:
            data = data.get('payload')

        data['data_issuer'] = data.get('issuer', None)
        data.pop('issuer', None)

        raw_bounty['deadline'] = datetime.datetime.fromtimestamp(raw_bounty.get('deadline', None))

        extra_data = {
            "bounty_id": id,
            "data": data_hash,
            "data_json": str(data_JSON),
            "arbiter": arbiter,
        }

        bounty_serializer = BountySerializer(data={**data, **raw_bounty, **extra_data})
        bounty_serializer.is_valid(raise_exception=True)
        bounty_serializer.save()

    def activate_bounty(self, id):
        bounty_response = StandardBounties.getBounty(id)
        raw_bounty = RawBountyData(*bounty_response)
        bounty = Bounty.objects.get(bounty_id=id)
        bounty.balance = raw_bounty.balance
        bounty.bountystage = raw_bounty.bountystage
        bounty.save()

    def fulfill_bounty(self, bounty_id, fulfillment_id):
        fulfillment = Fulfillment.objects.filter(
            fulfillment_id=fulfillment_id, bounty_id=bounty_id
        ).exists()
        if fulfillment:
            return
        fulfillment_response = StandardBounties.getFulfillment(bounty_id, fulfillment_id)
        fulfillment_data = RawFulfillmentData(*fulfillment_response)._asdict()
        data_hash = fulfillment_data.get('data')
        data_json = ipfs.cat(data_hash)
        data = json.loads(data_json)
        data['data_fulfiller'] = data.get('fulfiller', None)
        data.pop('fulfiller', None)
        if 'payload' in data:
            data = data.get('payload')
        extra_data = {
            'data_json': str(data_json),
            'fulfillment_id': fulfillment_id,
            'bounty': bounty_id,
        }
        fulfillment_serializer = FulfillmentSerializer(data={**data, **fulfillment_data, **extra_data})
        fulfillment_serializer.is_valid(raise_exception=True)
        fulfillment_serializer.save()

    def update_fulfillment(self, bounty_id, fulfillment_id):
        fulfillment_response = StandardBounties.getFulfillment(bounty_id, fulfillment_id)
        fulfillment_data = RawFulfillmentData(*fulfillment_response)._asdict()
        data_hash = fulfillment_data.data
        data_json = ipfs.cat(data_hash)
        data = json.loads(data_json)
        data['data_fulfiller'] = data.get('fulfiller', None)
        data.pop('fulfiller', None)
        fulfillment = Fulfillment.objects.get(fulfillment_id=fulfillment_id)
        fulfillment_serializer = FulfillmentSerializer(fulfillment, data={**data, **fulfillment_data, **{data_json: data_json}}, partial=True)
        fulfillment_serializer.save()

    def accept_fulfillmment(self, bounty_id, fulfillment_id):
        bounty_response = StandardBounties.getBounty(id)
        raw_bounty = RawBountyData(*bounty_response)
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.balance = bounty.balance - raw_bounty.fulfillmentAmount
        bounty.save()

        fulfillment = Fulfillment.objects.get(fulfillment_id=fulfillment_id)
        fulfillment.accepted = True
        fulfillment.save()

    def kill_bounty(self, bounty_id):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.old_balance = bounty.balance
        bounty.balance = 0
        bounty.save()

    def add_contribution(self, bounty_id):
        bounty_response = StandardBounties.getBounty(bounty_id)
        raw_bounty = RawBountyData(*bounty_response)
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.balance = raw_bounty.balance
        bounty.save()

    def extend_deadline(self, bounty_id):
        bounty_response = StandardBounties.getBounty(bounty_id)
        raw_bounty = RawBountyData(*bounty_response)
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.deadline = datetime.datetime.fromtimestamp(raw_bounty.deadline)
        bounty.save()

    def change_bounty(self, bounty_id):
        bounty_response = StandardBounties.getBounty(bounty_id)
        raw_bounty = RawBountyData(*bounty_response)._asdict()
        data_hash = StandardBounties.getBountyData(bounty_id)
        data_JSON = ipfs.cat(data_hash)
        data = json.loads(data_JSON)

        data['data_issuer'] = data.get('issuer', None)
        data.pop('issuer', None)

        extra_data = {
            "data": data_hash,
            "data_json": str(data_JSON),
        }

        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty_serializer = BountySerializer(bounty, data={**data, **extra_data}, partial=True)
        bounty_serializer.is_valid(raise_exception=True)
        bounty_serializer.save()

    def transfer_issuer(self, bounty_id):
        bounty_response = StandardBounties.getBounty(id)
        raw_bounty = RawBountyData(*bounty_response)._asdict()
        data_hash = StandardBounties.getBountyData(id)
        data_JSON = ipfs.cat(data_hash)
        data = json.loads(data_JSON)

        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.issuer = raw_bounty.issuer
        bounty.data_issuer = data.get('issuer', None)
        bounty.save()

    def increase_payout(self, bounty_id):
        bounty_response = StandardBounties.getBounty(bounty_id)
        raw_bounty = RawBountyData(*bounty_response)

        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.balance = raw_bounty.balance
        bounty.fulfillmentAmount = raw_bounty.fulfillmentAmount
