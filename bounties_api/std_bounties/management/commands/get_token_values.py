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
                bounty_stage__in=[DEAD_STAGE, COMPLETED_STAGE])
            for bounty in all_bounties:
                price = token_cache.get(bounty.token_symbol, None)
                if not price:
                    try:
                        current_token = Token.objects.get(symbol=bounty.token_symbol)
                        price = current_token.price_usd
                    except Token.DoesNotExist:
                        price = None

                if price is not None:
                    decimals = bounty.token_decimals
                    fulfillment_amount = bounty.fulfillment_amount
                    bounty.usd_price = (
                        fulfillment_amount / Decimal(pow(10, decimals))) * Decimal(price)
                    bounty.tokenLockPrice = None
                    bounty.save()
                # maybe a token was not added to coinmarketcap until later
                if price is not None and not bounty.token:
                    token_model = Token.objects.get(symbol=bounty.token_symbol)
                    bounty.token = token_model
                    bounty.save()

            all_draft_bounties = DraftBounty.objects.filter(on_chain=False)
            for draft_bounty in all_draft_bounties:
                price = token_cache.get(draft_bounty.token_symbol, None)
                if price is not None:
                    decimals = draft_bounty.token_decimals
                    fulfillment_amount = draft_bounty.fulfillment_amount
                    draft_bounty.usd_price = (
                        fulfillment_amount / Decimal(pow(10, decimals))) * Decimal(price)
                    draft_bounty.save()
                # maybe a token was not added to coinmarketcap until later
                if price is not None and not draft_bounty.token:
                    token_model = Token.objects.get(
                        symbol=draft_bounty.token_symbol)
                    draft_bounty.token = token_model
                    draft_bounty.save()

        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
