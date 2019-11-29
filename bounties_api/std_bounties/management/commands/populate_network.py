import requests
from math import pow
from decimal import Decimal
from django.core.management.base import BaseCommand
from std_bounties.models import Bounty, Fulfillment
import logging
import sys

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Update the views counts on bounties'

    def handle(self, *args, **options):
        try:
            all_bounties = Bounty.objects.all()
            for bounty in all_bounties:
                bounty.network = 'mainNet'
                bounty.save()
            all_fulfillments = Fulfillment.objects.all()
            for fulfillment in all_fulfillments:
                fulfillment.network = 'mainNet'
                fulfillment.save()
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
