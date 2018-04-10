import requests
from math import pow
from decimal import Decimal
from django.core.management.base import BaseCommand
from std_bounties.constants import DEAD_STAGE, COMPLETED_STAGE
from std_bounties.models import Token, Bounty
import logging

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Update current token values, and update usd_price on all bounties'

    def handle(self, *args, **options):
        try:
            token_cache = {}
            r = requests.get(
                'https://api.coinmarketcap.com/v1/ticker/?convert=USD&limit=1000000')
            r.raise_for_status()
            coins = r.json()
            for coin in coins:
                symbol = coin['symbol']
                price_usd = coin['price_usd']
                coin_data = {
                    'normalized_name': coin['id'],
                    'name': coin['name'],
                    'symbol': symbol,
                }

                token_cache[symbol] = price_usd
                Token.objects.update_or_create(
                    **coin_data, defaults={'price_usd': price_usd})

            all_bounties = Bounty.objects.exclude(
                bountyStage__in=[DEAD_STAGE, COMPLETED_STAGE])
            for bounty in all_bounties:
                price = token_cache.get(bounty.tokenSymbol, None)
                if price is not None:
                    decimals = bounty.tokenDecimals
                    fulfillmentAmount = bounty.fulfillmentAmount
                    bounty.usd_price = (
                        fulfillmentAmount / Decimal(pow(10, decimals))) * Decimal(price)
                    bounty.tokenLockPrice = None
                    bounty.save()
                # maybe a token was not added to coinmarketcap until later
                if price is not None and not bounty.token:
                    token_model = Token.objects.get(symbol=bounty.tokenSymbol)
                    bounty.token = token_model
                    bounty.save()

        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
