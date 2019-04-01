import json
import requests
from decimal import Decimal
from datetime import datetime

from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from web3.middleware import geth_poa_middleware
from std_bounties.constants import rev_mapped_difficulties, BEGINNER, INTERMEDIATE, ADVANCED
from std_bounties.contract import data
from std_bounties.models import Token
from utils.functional_tools import pluck

from django.conf import settings
import ipfsapi
import logging


logger = logging.getLogger('django')

web3 = Web3(HTTPProvider(settings.ETH_NETWORK_URL))
if settings.ETH_NETWORK in ['rinkeby', 'consensysrinkeby', 'rinkebystaging', 'rinkeby-dev']:
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
bounties_json = json.loads(data)
ipfs = ipfsapi.connect(host='https://ipfs.infura.io')
bounty_v0_data_keys = [
    'uid',
    'description',
    'title',
    'sourceFileName',
    'sourceFileHash',
    'sourceDirectoryHash',
    'webReferenceURL'
]

bounty_v1_data_keys = [

]

fulfillment_data_keys = [
    'description',
    'url',
    'sourceFileName',
    'sourceFileHash',
    'sourceDirectoryHash'
]


def map_bounty_data(ipfs_hash, bounty_id):
    if len(ipfs_hash) != 46 or not ipfs_hash.startswith('Qm'):
        logger.error('Data Hash Incorrect for bounty: {:d}'.format(bounty_id))
        return {}

    raw_ipfs_data = ipfs.cat(ipfs_hash)

    data = json.loads(raw_ipfs_data)
    meta = data.get('meta', {})

    schema_version = meta.get('schemaVersion', '0.1')

    if schema_version == '0.1' or schema_version != '1.0':
        if 'payload' in data:
            data = data.get('payload')

        metadata = data.get('metadata', {})

        experienceLevel = metadata.get('experienceLevel') or data.get('difficulty') or ''
        experienceLevel = 'Advanced' if experienceLevel == 'Expert' else experienceLevel

        formattedExperienceLevel = str(experienceLevel).lower().strip().capitalize()

        metadata.update({'experienceLevel': rev_mapped_difficulties.get(formattedExperienceLevel, BEGINNER)})

        data_issuer = data.get('issuer', {})
        if isinstance(data_issuer, str):
            logger.error('Issuer schema incorrect for: {:d}'.format(bounty_id))
            data_issuer = {}

        categories = data.get('categories', [])
        plucked_data = pluck(data, bounty_v0_data_keys)

        bounty = {
            **plucked_data,
            **meta,
            **metadata,
            'private_fulfillments': data.get('privateFulfillments', True),
            'fulfillers_need_approval': data.get('fulfillersNeedApproval', False),
            'issuer_name': data_issuer.get('name', ''),
            'issuer_email': data_issuer.get('email', '') or data.get('contact', ''),
            'issuer_githubUsername': data_issuer.get('githubUsername', ''),
            'issuer_address': data_issuer.get('address', ''),
            'revisions': data.get('revisions', None),
            'data_issuer': data_issuer,
            'data': ipfs_hash,
            'raw_ipfs_data': str(raw_ipfs_data),
            'data_categories': categories,
            'schema_version': schema_version,
            'schema_name': meta.get('schemaname', ''),
        }

        # if 'platform' is gitcoin, also return deadline
        if meta.get('platform', '') == 'gitcoin' and 'expire_date' in data:
            bounty.update({'deadline': datetime.utcfromtimestamp(int(data.get('expire_date')))})
        if meta.get('platform', '') == 'gitcoin':
            bounty.update({'private_fulfillments': False})
    elif schema_version == '1.0':
        payload = data.get('payload')
        meta = data.get('meta')

        difficulty = int(payload.get('difficulty'))
        if difficulty == 3:
            difficulty = ADVANCED
        elif difficulty == 2:
            difficulty = INTERMEDIATE
        else:
            difficulty = BEGINNER

        bounty = {
            # required
            'title': payload.get('title'),
            'description': payload.get('description'),
            'fulfillment_amount': int(payload.get('fulfillment_amount')),

            'revisions': payload.get('expectedRevisions'),
            'difficulty': difficulty,
            'private_fulfillments': payload.get('privateFulfillments'),
            'fulfillers_need_approval': payload.get('fulfillersNeedApproval'),

            # optional
            'categories': payload.get('categories', []),
            'attached_filename': payload.get('ipfsFilename', None),
            'attached_data_hash': payload.get('ipfsHash', None),
            'attached_url': payload.get('webReferenceURL', None),

            # meta
            'schema_version': schema_version,
            'schema_name': meta.get('schemaname'),
            'platform': meta.get('platform'),
        }

    return bounty


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
    plucked_data = pluck(data, fulfillment_data_keys)

    return {
        'data_json': str(data_JSON),
        'data': ipfs_hash,
        'data_fulfiller': data_fulfiller,
        'fulfiller_name': data_fulfiller.get('name', ''),
        'fulfiller_email': data_fulfiller.get('email', '') or data.get('contact', ''),
        'fulfiller_githubUsername': data_fulfiller.get('githubUsername', ''),
        'fulfiller_address': data_fulfiller.get('address', ''),
        **plucked_data,
        **metadata,
    }


def calculate_token_quantity(value, decimals):
    return Decimal(value) / Decimal(pow(10, decimals))


def calculate_usd_price(value, decimals, usd_rate):
    return ((Decimal(value) / Decimal(pow(10, decimals))) * Decimal(usd_rate)).quantize(Decimal(10) ** -8)


def get_token_pricing(token_symbol, token_decimals, value):
    try:
        token_model = Token.objects.filter(symbol=token_symbol).earliest('id')
        usd_price = calculate_usd_price(
            value,
            token_decimals,
            token_model.price_usd
        )
    except Token.DoesNotExist:
        token_model = None
        usd_price = 0

    return usd_price, token_model


def get_historic_pricing(token_symbol, token_decimals, value, timestamp):
    r = requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym={}&tsyms=USD&ts={}&extraParams=bountiesnetwork'.format(
        token_symbol,
        timestamp
    ))

    r.raise_for_status()

    coin_data = r.json()

    if coin_data.get('Response', None) == 'Error':
        usd_price, token_model = get_token_pricing(token_symbol, token_decimals, value)
        token_price = token_model.price_usd if token_model else 0
        return usd_price, token_price

    token_price = coin_data[token_symbol]['USD']

    return calculate_usd_price(value, token_decimals, token_price), token_price


def map_token_data(version, token_contract, amount):
    token_symbol = 'ETH'
    token_decimals = 18

    if version == '0':
        pass
    elif version == '20':
        HumanStandardToken_abi = bounties_json['interfaces']['HumanStandardToken']
        DSToken_abi = bounties_json['interfaces']['DSToken']

        try:
            HumanStandardToken = web3.eth.contract(
                abi=HumanStandardToken_abi,
                address=web3.toChecksumAddress(token_contract),
                ContractFactoryClass=ConciseContract
            )

            token_symbol = HumanStandardToken.symbol()
            token_decimals = HumanStandardToken.decimals()

        except OverflowError:
            DSToken = web3.eth.contract(
                abi=DSToken_abi,
                address=web3.toChecksumAddress(token_contract),
                ContractFactoryClass=ConciseContract
            )

            # Symbol in DSToken contract is bytes32 and unused chars are padded
            # with '\x00'
            token_symbol = DSToken.symbol().decode().rstrip('\x00')
            token_decimals = DSToken.decimals()
    elif version == '721':
        # todo
        pass
    else:
        raise 'unknown token type'

    usd_price, token_model = get_token_pricing(
        token_symbol,
        token_decimals,
        amount
    )

    return {
        'token_symbol': token_symbol,
        'token_decimals': token_decimals,
        'token': token_model.id if token_model else None,
        'token_version': version,
        'usd_price': usd_price,
    }
