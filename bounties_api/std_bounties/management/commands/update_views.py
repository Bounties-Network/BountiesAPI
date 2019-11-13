import requests
from math import pow
from decimal import Decimal
from django.core.management.base import BaseCommand
from std_bounties.models import View, Bounty, Fulfillment
import logging
import sys

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Update the views counts on bounties'

    def handle(self, *args, **options):
        try:
            all_bounties = Bounty.objects.all()
            for bounty in all_bounties:
                fulfillment_count = Fulfillment.objects.filter(bounty_id=bounty.id).count()
                if bounty.view_count is None:
                    bounty.view_count = fulfillment_count
                elif (bounty.view_count < fulfillment_count):
                    bounty.view_count += fulfillment_count
                bounty.save()
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
