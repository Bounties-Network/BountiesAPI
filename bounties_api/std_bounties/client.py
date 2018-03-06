import json
import datetime
from decimal import Decimal
from collections import namedtuple
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from std_bounties.contract import data
from std_bounties.models import Bounty, Fulfillment
from std_bounties.serializers import BountySerializer, FulfillmentSerializer
from std_bounties.constants import DRAFT_STAGE, ACTIVE_STAGE, DEAD_STAGE, COMPLETED_STAGE, EXPIRED_STAGE
from bounties.utils import getDateTimeFromTimestamp
from django.conf import settings
from django.db import transaction
import ipfsapi
import logging

logger = logging.getLogger('django')


web3 = Web3(HTTPProvider(settings.ETH_NETWORK_URL))
RawFulfillmentData = namedtuple('RawFulfillmentData', ['accepted', 'fulfiller', 'data'])
bounties_json = json.loads(data)
StandardBounties = web3.eth.contract(
    bounties_json['interfaces']['StandardBounties'],
    bounties_json[settings.ETH_NETWORK]['standardBountiesAddress']['v1'],
    ContractFactoryClass=ConciseContract
)
ipfs = ipfsapi.connect(host='https://ipfs.infura.io')

class BountyClient:

    def __init__(self):
        pass

    @transaction.atomic
    def issue_bounty(self, bounty_id, inputs, event_timestamp):
        bounty = Bounty.objects.filter(bounty_id=bounty_id).exists()
        if bounty:
            return

        bounty_data = inputs.copy()
        data_hash = bounty_data.get('data', 'invalid')
        if len(data_hash) != 46 or not data_hash.startswith('Qm'):
            logger.error('Data Hash Incorrect for bounty: {:d}'.format(bounty_id))
            data_JSON = "{}"
        else:
            data_JSON = ipfs.cat(data_hash)
        if len(data_hash) == 0:
            bounty_data['data'] = 'invalid'

        data = json.loads(data_JSON)
        metadata = data.get('meta', {})
        if 'payload' in data:
            data = data.get('payload')

        data['data_issuer'] = data.get('issuer', None)
        data.pop('issuer', None)
        data['bounty_created'] = datetime.datetime.fromtimestamp(int(event_timestamp))
        data.pop('created', None)
        data['data_categories'] = data.get('categories', [])
        categories = data.pop('categories', [])

        bounty_data['deadline'] = getDateTimeFromTimestamp(bounty_data.get('deadline', None))
        bounty_data.pop('value', None)

        extra_data = {
            'bounty_id': bounty_id,
            'data_json': str(data_JSON),
            'bountyStage': DRAFT_STAGE,
        }

        bounty_serializer = BountySerializer(data={**data, **bounty_data, **extra_data, **metadata})
        bounty_serializer.is_valid(raise_exception=True)
        saved_bounty = bounty_serializer.save()
        saved_bounty.save_and_clear_categories(categories)


    def activate_bounty(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.bountyStage = ACTIVE_STAGE
        bounty.save()

    def fulfill_bounty(self, bounty_id, fulfillment_id, inputs, event_timestamp):
        fulfillment = Fulfillment.objects.filter(
            fulfillment_id=fulfillment_id, bounty_id=bounty_id
        ).exists()
        if fulfillment:
            return

        fulfillment_response = StandardBounties.getFulfillment(bounty_id, fulfillment_id)
        fulfillment_data = RawFulfillmentData(*fulfillment_response)._asdict()

        data_hash = inputs.get('data')
        data_json = ipfs.cat(data_hash)
        data = json.loads(data_json)
        data['data_fulfiller'] = data.get('fulfiller', None)
        data.pop('fulfiller', None)
        metadata = data.pop('meta', {})
        if 'payload' in data:
            data = data.get('payload')

        extra_data = {
            'data_json': str(data_json),
            'fulfillment_id': fulfillment_id,
            'fulfiller': fulfillment_data.get('fulfiller'),
            'bounty': bounty_id,
            'data': data_hash,
            'accepted': False,
            'fulfillment_created':  datetime.datetime.fromtimestamp(int(event_timestamp)),
        }

        fulfillment_serializer = FulfillmentSerializer(data={**data, **extra_data, **metadata})
        fulfillment_serializer.is_valid(raise_exception=True)
        fulfillment_serializer.save()

    def update_fulfillment(self, bounty_id, fulfillment_id, inputs):
        data_hash = inputs.get('data')
        data_json = ipfs.cat(data_hash)
        data = json.loads(data_json)
        data['data_fulfiller'] = data.get('fulfiller', None)
        data.pop('fulfiller', None)
        metadata = data.pop('meta', {})

        fulfillment = Fulfillment.objects.get(fulfillment_id=fulfillment_id, bounty_id=bounty_id)
        fulfillment_serializer = FulfillmentSerializer(fulfillment,
            data={**data, **metadata, **{data_json: data_json, data: data_hash}}, partial=True
        )
        fulfillment_serializer.save()

    def accept_fulfillment(self, bounty_id, fulfillment_id):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.balance = bounty.balance - bounty.fulfillmentAmount
        if bounty.balance < bounty.fulfillmentAmount:
            bounty.bountyStage = COMPLETED_STAGE
        bounty.save()

        fulfillment = Fulfillment.objects.get(bounty_id=bounty_id, fulfillment_id=fulfillment_id)
        fulfillment.accepted = True
        fulfillment.save()

    def kill_bounty(self, bounty_id):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.old_balance = bounty.balance
        bounty.balance = 0
        bounty.bountyStage = DEAD_STAGE
        bounty.save()

    def add_contribution(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.balance = Decimal(inputs.get('value'))
        if bounty.balance >= bounty.fulfillmentAmount and bounty.bountyStage == EXPIRED_STAGE:
            bounty.bountyStage = ACTIVE_STAGE
        bounty.save()

    def extend_deadline(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.deadline = getDateTimeFromTimestamp(inputs.get('newDeadline', None))
        bounty.save()

    @transaction.atomic
    def change_bounty(self, bounty_id, inputs):
        data = {}
        updated_data = {}
        metadata = {}
        data_hash = inputs.get('data', None)
        deadline = inputs.get('newDeadline', None)
        fulfillmentAmount = inputs.get('newFulfillmentAmount', None)
        arbiter = inputs.get('newArbiter', None)

        if data_hash:
            data_JSON = ipfs.cat(data_hash)
            data = json.loads(data_JSON)
            metadata = data.get('meta', {})
            if 'payload' in data:
                data = data.get('payload')

            data['data_issuer'] = data.get('issuer', None)
            data.pop('issuer', None)
            data['data_categories'] = data.get('categories', None)
            categories = data.pop('categories', None)
            updated_data['data'] = data_hash
            updated_data['data_json'] = str(data_JSON)

        if deadline:
            updated_data['deadline'] = datetime.datetime.fromtimestamp(int(new_deadline))

        if fulfillmentAmount:
            updated_data['fulfillmentAmount'] = Decimal(fulfillmentAmount)

        if arbiter:
            updated_data['arbiter'] = arbiter

        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty_serializer = BountySerializer(bounty, data={**data, **updated_data, **metadata}, partial=True)
        bounty_serializer.is_valid(raise_exception=True)
        saved_bounty = bounty_serializer.save()
        if data_hash:
            saved_bounty.save_and_clear_categories(categories)


    def transfer_issuer(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.issuer = inputs.get('newIssuer')
        bounty.save()

    def increase_payout(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        value = inputs.get('value')
        if value:
            bounty.balance = bounty.balance + Decimal(value)
        bounty.fulfillmentAmount = Decimal(inputs.get('fulfillmentAmount'))
        bounty.save()
