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
    help = 'recreate all tokens'

    def handle(self, *args, **options):
        try:
            all_bounties = Bounty.objects.all()
            for bounty in all_bounties:
                try:
                    token = Token.objects.get(address=bounty.token_contract.lower())
                    bounty.token_id = token.id
                    bounty.token_contract = bounty.token_contract.lower()
                    bounty.save() # existing token with that address was created and saved, use that one
                except Token.DoesNotExist: # no existing token exists with that address
                    if bounty.token_id is not None: # bounty has a token, just hasn't had its details populated
                        token = Token.objects.get(id=bounty.token_id)
                        token.address = bounty.token_contract.lower()
                        token.decimals = bounty.token_decimals
                        token.save()
                    else: # bounty has token and address, but no token with that address exists yet
                        token = Token.objects.create(
                            address=bounty.token_contract.lower(),
                            name=bounty.token_symbol,
                            symbol=bounty.token_symbol,
                            price_usd=0,
                            decimals=bounty.token_decimals
                        )
                        bounty.token_id = token.id
                        bounty.token_contract = token.address
            all_tokens = Token.objects.all()
            for token in all_tokens:
                bounties_with_token = Bounty.objects.filter(token_id=token.id).count()
                if bounties_with_token == 0:
                    token.delete()
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
