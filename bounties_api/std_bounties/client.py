import json
import datetime
from decimal import Decimal
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from std_bounties.contract import data
from std_bounties.models import Bounty, Fulfillment, Token
from std_bounties.serializers import BountySerializer, FulfillmentSerializer
from std_bounties.constants import DRAFT_STAGE, ACTIVE_STAGE, DEAD_STAGE, COMPLETED_STAGE, EXPIRED_STAGE
from std_bounties.client_helpers import map_bounty_data, map_token_data, get_token_pricing
from bounties.utils import getDateTimeFromTimestamp
from django.conf import settings
from django.db import transaction
import ipfsapi
import logging


logger = logging.getLogger('django')

web3 = Web3(HTTPProvider(settings.ETH_NETWORK_URL))
bounties_json = json.loads(data)
ipfs = ipfsapi.connect(host='https://ipfs.infura.io')
data_keys = ['description', 'title', 'sourceFileName', 'sourceFileHash', 'sourceDirectoryHash', 'webReferenceUrl']
issue_bounty_input_keys = ['fulfillmentAmount', 'arbiter', 'paysTokens', 'tokenContract', 'value']

class BountyClient:

    def __init__(self):
        pass

    @transaction.atomic
    def issue_bounty(self, bounty_id, inputs, event_timestamp):
        bounty = Bounty.objects.filter(bounty_id=bounty_id).exists()
        if bounty:
            return

        data_hash = inputs.get('data', 'invalid')
        ipfs_data = map_bounty_data(data_hash)
        token_data = map_token_data(inputs.get('paysTokens'), inputs.get('tokenContract'), inputs.get('fulfillmentAmount'))

        plucked_inputs = { key: inputs.get(key) for key in issue_bounty_input_keys }

        bounty_data = {
            'id': bounty_id,
            'bounty_id': bounty_id,
            'issuer':  inputs.get('issuer', '').lower(),
            'deadline': getDateTimeFromTimestamp(inputs.get('deadline', None)),
            'bountyStage': DRAFT_STAGE,
            'bounty_created': datetime.datetime.fromtimestamp(int(event_timestamp)),
        }

        bounty_serializer = BountySerializer(data={**bounty_data, **plucked_inputs, **ipfs_data, **token_data})
        bounty_serializer.is_valid(raise_exception=True)
        saved_bounty = bounty_serializer.save()
        saved_bounty.save_and_clear_categories(ipfs_data.get('data_categories'))


    def activate_bounty(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.bountyStage = ACTIVE_STAGE
        bounty.save()


    def fulfill_bounty(self, bounty_id, fulfillment_id, inputs, event_timestamp, transaction_issuer):
        fulfillment = Fulfillment.objects.filter(
            fulfillment_id=fulfillment_id, bounty_id=bounty_id
        ).exists()
        if fulfillment:
            return

        print('hola')
        print(inputs)

        data_hash = inputs.get('data')
        data_json = ipfs.cat(data_hash)
        data = json.loads(data_json)
        metadata = data.pop('meta', {})
        if 'payload' in data:
            data = data.get('payload')
        data_fulfiller = data.get('fulfiller', {})
        data['data_fulfiller'] = data_fulfiller
        data.pop('fulfiller', None)

        extra_data = {
            'data_json': str(data_json),
            'fulfillment_id': fulfillment_id,
            'fulfiller': transaction_issuer.lower(),
            'bounty': bounty_id,
            'data': data_hash,
            'accepted': False,
            'fulfillment_created':  datetime.datetime.fromtimestamp(int(event_timestamp)),
            'fulfiller_name': data_fulfiller.get('name', ''),
            'fulfiller_email': data_fulfiller.get('email', '') or data.get('contact', ''),
            'fulfiller_githubUsername': data_fulfiller.get('githubUsername', ''),
            'fulfiller_address': data_fulfiller.get('address', ''),
        }

        fulfillment_serializer = FulfillmentSerializer(data={**data, **extra_data, **metadata, **data_fulfiller})
        fulfillment_serializer.is_valid(raise_exception=True)
        fulfillment_serializer.save()


    def update_fulfillment(self, bounty_id, fulfillment_id, inputs):
        data_hash = inputs.get('data')
        data_json = ipfs.cat(data_hash)
        data = json.loads(data_json)
        metadata = data.pop('meta', {})
        if 'payload' in data:
            data = data.get('payload')
        data_fulfiller = data.get('fulfiller', {})
        data['data_fulfiller'] = data_fulfiller
        data.pop('fulfiller', None)

        extra_data = {
            'fulfiller_name': data_fulfiller.get('name', ''),
            'fulfiller_email': data_fulfiller.get('email', '') or data.get('contact', ''),
            'fulfiller_githubUsername': data_fulfiller.get('githubUsername', ''),
            'fulfiller_address': data_fulfiller.get('address', ''),
        }

        fulfillment = Fulfillment.objects.get(fulfillment_id=fulfillment_id, bounty_id=bounty_id)
        fulfillment_serializer = FulfillmentSerializer(fulfillment,
            data={**data, **metadata, **{data_json: data_json, data: data_hash} **extra_data}, partial=True
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
        updated_data = {}
        data_hash = inputs.get('data', None)
        deadline = inputs.get('newDeadline', None)
        fulfillmentAmount = inputs.get('newFulfillmentAmount', None)
        arbiter = inputs.get('newArbiter', None)

        if data_hash:
            updated_data = map_bounty_data(data_hash)

        if deadline:
            updated_data['deadline'] = datetime.datetime.fromtimestamp(int(new_deadline))

        if fulfillmentAmount:
            updated_data['fulfillmentAmount'] = Decimal(fulfillmentAmount)

        if arbiter:
            updated_data['arbiter'] = arbiter

        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty_serializer = BountySerializer(bounty, data=updated_data, partial=True)
        bounty_serializer.is_valid(raise_exception=True)
        saved_bounty = bounty_serializer.save()

        if data_hash:
            saved_bounty.save_and_clear_categories(updated_data.get('data_categories'))

        if fulfillmentAmount:
            usd_price = get_token_pricing(saved_bounty.tokenSymbol, saved_bounty.tokenDecimals, fulfillmentAmount)[0]
            saved_bounty.usd_price = usd_price
            saved_bounty.save()


    def transfer_issuer(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty.issuer = inputs.get('newIssuer')
        bounty.save()


    def increase_payout(self, bounty_id, inputs):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        value = inputs.get('value')
        if value:
            bounty.balance = bounty.balance + Decimal(value)
        bounty.fulfillmentAmount = Decimal(inputs.get('newFulfillmentAmount'))
        bounty.save()
