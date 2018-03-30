import json
import datetime
from decimal import Decimal
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from std_bounties.contract import data
from std_bounties.models import Token
from bounties.utils import getDateTimeFromTimestamp
from django.conf import settings
import ipfsapi
import logging


logger = logging.getLogger('django')

web3 = Web3(HTTPProvider(settings.ETH_NETWORK_URL))
bounties_json = json.loads(data)
ipfs = ipfsapi.connect(host='https://ipfs.infura.io')
bounty_data_keys = [
    'description',
    'title',
    'sourceFileName',
    'sourceFileHash',
    'sourceDirectoryHash',
    'webReferenceUrl']
fulfillment_data_keys = [
    'description',
    'sourceFileName',
    'sourceFileHash',
    'sourceDirectoryHash']


def map_bounty_data(data_hash, bounty_id):
    ipfs_hash = data_hash
    if len(ipfs_hash) != 46 or not ipfs_hash.startswith('Qm'):
        logger.error('Data Hash Incorrect for bounty: {:d}'.format(bounty_id))
        data_JSON = "{}"
    else:
        data_JSON = ipfs.cat(ipfs_hash)
    if len(ipfs_hash) == 0:
        ipfs_hash = 'invalid'

    data = json.loads(data_JSON)
    metadata = data.get('meta', {})
    if 'payload' in data:
        data = data.get('payload')

    data_issuer = data.get('issuer', {})
    if isinstance(data_issuer, str):
        logger.error('Issuer schema incorrect for: {:d}'.format(bounty_id))
        data_issuer = {}

    categories = data.get('categories', [])
    plucked_data = {key: data.get(key, '') for key in bounty_data_keys}

    return {
        **plucked_data,
        **metadata,
        'issuer_name': data_issuer.get(
            'name',
            ''),
        'issuer_email': data_issuer.get(
            'email',
            '') or data.get(
                'contact',
                ''),
        'issuer_githubUsername': data_issuer.get(
            'githubUsername',
            ''),
        'issuer_address': data_issuer.get(
            'address',
            ''),
        'data_issuer': data_issuer,
        'data': ipfs_hash,
        'data_json': str(data_JSON),
        'data_categories': categories,
    }


def map_fulfillment_data(data_hash, bounty_id, fulfillment_id):
    ipfs_hash = data_hash
    if len(ipfs_hash) != 46 or not ipfs_hash.startswith('Qm'):
        logger.error(
            'Data Hash Incorrect for fulfillment on bounty: {:d} fulfillment: {:d}'.format(
                bounty_id, fulfillment_id))
        data_JSON = "{}"
    else:
        data_JSON = ipfs.cat(ipfs_hash)
    if len(ipfs_hash) == 0:
        ipfs_hash = 'invalid'

    data = json.loads(data_JSON)
    metadata = data.pop('meta', {})
    if 'payload' in data:
        data = data.get('payload')
    data_fulfiller = data.get('fulfiller', {})
    plucked_data = {key: data.get(key, '') for key in fulfillment_data_keys}

    return {
        'data_json': str(data_JSON),
        'data': ipfs_hash,
        'data_fulfiller': data_fulfiller,
        'fulfiller_name': data_fulfiller.get(
            'name',
            ''),
        'fulfiller_email': data_fulfiller.get(
            'email',
            '') or data.get(
                'contact',
                ''),
        'fulfiller_githubUsername': data_fulfiller.get(
            'githubUsername',
            ''),
        'fulfiller_address': data_fulfiller.get(
            'address',
            ''),
        **plucked_data,
        **metadata,
    }


def get_token_pricing(token_symbol, token_decimals, value):
    try:
        token_model = Token.objects.get(symbol=token_symbol)
        usd_price = ((Decimal(value) / Decimal(pow(10, token_decimals)))
                     * Decimal(token_model.price_usd)).quantize(Decimal(10) ** -8)
    except Token.DoesNotExist:
        token_model = None
        usd_price = 0

    return usd_price, token_model


def map_token_data(pays_tokens, token_contract, amount):
    token_symbol = 'ETH'
    token_decimals = 18
    token_price = 0
    if pays_tokens:
        HumanStandardToken = web3.eth.contract(
            bounties_json['interfaces']['HumanStandardToken'],
            token_contract,
            ContractFactoryClass=ConciseContract
        )
        # putting up a bounty to solve this. This is a weird bug on the DAI symbol call 
        if token_contract == '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359':
            token_symbol = 'DAI'
        else:
            token_symbol = token_symbol = HumanStandardToken.symbol()
        token_decimals = HumanStandardToken.decimals()

    usd_price, token_model = get_token_pricing(
        token_symbol, token_decimals, amount)

    return {
        'tokenSymbol': token_symbol,
        'tokenDecimals': token_decimals,
        'token': token_model.id if token_model else None,
        'usd_price': usd_price,
    }
