import requests
from math import pow
from decimal import Decimal
from django.core.management.base import BaseCommand
from std_bounties.constants import DEAD_STAGE, COMPLETED_STAGE
from std_bounties.models import Token, Bounty, DraftBounty
import logging
import sys

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'recreate all token values'

    def handle(self, *args, **options):
        try:
            all_bounties = Bounty.objects.all()
            for bounty in all_bounties:
                if bounty.token_id is None:
                    token, created = Token.objects.get_or_create(
                        address=bounty.token_contract,
                        defaults={
                            'address': bounty.token_contract,
                            'name': bounty.token_symbol,
                            'symbol': bounty.token_symbol,
                            'price_usd': 0,
                            'decimals': bounty.token_decimals
                        }
                    )
                    r = requests.get('https://api.coingecko.com/api/v3/coins/ethereum/contract/' + bounty.token_contract)
                    if r.status_code == 200:
                        response = r.json()
                        token.name = response["name"]
                        token.symbol = response["symbol"].upper()
                        token.price_usd = response["market_data"]["current_price"]["usd"]
                        token.save()
                else:
                    token = Token.objects.get(id=bounty.token_id)
                    token.symbol = bounty.token_symbol
                    token.address = bounty.token_contract
                    token.decimals = bounty.token_decimals
                    r = requests.get('https://api.coingecko.com/api/v3/coins/ethereum/contract/' + bounty.token_contract)
                    if r.status_code == 200:
                        print('response')
                        print(r.json())
                        response = r.json()
                        token.name = response["name"]
                        token.symbol = response["symbol"].upper()
                        token.price_usd = response["market_data"]["current_price"]["usd"]
                    token.save()
            all_tokens = Token.objects.all()
            for token in all_tokens:
                if token.address is None:
                    token.delete()
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
