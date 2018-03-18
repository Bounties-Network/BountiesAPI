import json
import datetime
from decimal import Decimal
from collections import namedtuple
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from std_bounties.contract import data
from std_bounties.models import Bounty, Fulfillment, Token
from std_bounties.serializers import BountySerializer, FulfillmentSerializer
from std_bounties.constants import DRAFT_STAGE, ACTIVE_STAGE, DEAD_STAGE, COMPLETED_STAGE, EXPIRED_STAGE
from bounties.utils import getDateTimeFromTimestamp
from django.conf import settings
from django.db import transaction
import ipfsapi
import logging


logger = logging.getLogger('django')

web3 = Web3(HTTPProvider(settings.ETH_NETWORK_URL))
bounties_json = json.loads(data)
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
        bounty_data['issuer'] = bounty_data.get('issuer', '').lower()
        data_hash = bounty_data.get('data', 'invalid')
        if len(data_hash) != 46 or not data_hash.startswith('Qm'):
            logger.error('Data Hash Incorrect for bounty: {:d}'.format(bounty_id))
            data_JSON = "{}"
        else:
            data_JSON = ipfs.cat(data_hash)
        if len(data_hash) == 0:
            bounty_data['data'] = 'invalid'

        token_symbol = 'ETH'
        token_decimals = 18
        if inputs['paysTokens']:
            HumanStandardToken = web3.eth.contract(
                bounties_json['interfaces']['HumanStandardToken'],
                inputs['tokenContract'],
                ContractFactoryClass=ConciseContract
            )
            token_symbol = HumanStandardToken.symbol()
            token_decimals = HumanStandardToken.decimals()

        data = json.loads(data_JSON)
        metadata = data.get('meta', {})
        if 'payload' in data:
            data = data.get('payload')

        data_issuer =  data.get('issuer', {})
        if type(data_issuer) == str:
            logger.error('Issuer schema incorrect for: {:d}'.format(bounty_id))
            data_issuer = {}
        data['data_issuer'] = data_issuer
        data.pop('issuer', None)
        data['bounty_created'] = datetime.datetime.fromtimestamp(int(event_timestamp))
        data.pop('created', None)
        data['data_categories'] = data.get('categories', [])
        data.pop('tokenSymbol', None)
        categories = data.pop('categories', [])

        bounty_data['deadline'] = getDateTimeFromTimestamp(bounty_data.get('deadline', None))
        bounty_data.pop('value', None)

        token_price = 0
        try:
            token_model = Token.objects.get(symbol=token_symbol)
            token_price = ((Decimal(bounty_data.get('fulfillmentAmount')) / Decimal(pow(10, token_decimals))) * Decimal(token_model.price_usd)).quantize(Decimal(10) ** -8)
        except Token.DoesNotExist:
            token_model = None
            pass

        extra_data = {
            'id': bounty_id,
            'bounty_id': bounty_id,
            'data_json': str(data_JSON),
            'bountyStage': DRAFT_STAGE,
            'issuer_name': data_issuer.get('name', ''),
            'issuer_email': data_issuer.get('email', '') or data.get('contact', ''),
            'issuer_githubUsername': data_issuer.get('githubUsername', ''),
            'issuer_address': data_issuer.get('address', ''),
            'tokenSymbol': token_symbol,
            'tokenDecimals': token_decimals,
            'token': token_model.id if token_model else None,
            'usd_price': token_price,
        }

        bounty_serializer = BountySerializer(data={**data, **bounty_data, **extra_data, **metadata, **data_issuer})
        bounty_serializer.is_valid(raise_exception=True)
        saved_bounty = bounty_serializer.save()
        saved_bounty.save_and_clear_categories(categories)

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

            data_issuer = data.get('issuer', None)
            data['data_issuer'] = data_issuer
            data.pop('issuer', None)
            data['data_categories'] = data.get('categories', None)
            categories = data.pop('categories', None)
            data.pop('tokenSymbol', None)
            updated_data['data'] = data_hash
            updated_data['data_json'] = str(data_JSON)
            updated_data['fulfiller_name'] = data_fulfiller.get('name', '')
            updated_data['fulfiller_email'] = data_fulfiller.get('email', '') or data.get('contact', '')
            updated_data['fulfiller_githubUsername'] = data_fulfiller.get('githubUsername', '')
            updated_data['fulfiller_address'] = data_fulfiller.get('address', '')

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

        if fulfillmentAmount:
            try:
                token_model = Token.objects.get(symbol=saved_bounty.tokenSymbol)
                fulfillment_price = ((Decimal(fulfillmentAmount) / Decimal(pow(10, saved_bounty.tokenDecimals))) * Decimal(token_model.price_usd)).quantize(Decimal(10) ** -8)
                saved_bounty.usd_price = fulfillment_price
            except Token.DoesNotExist:
                token_price = 0
                pass


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
