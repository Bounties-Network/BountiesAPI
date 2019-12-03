import requests
from math import pow
from decimal import Decimal
from django.core.management.base import BaseCommand
from std_bounties.models import Activity, Community, Bounty, Event, Comment, Fulfillment, FulfillerApplication
import logging
import sys

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'delete the activities table'

    def handle(self, *args, **options):
        try:
            all_activities = Activity.objects.all().delete()
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
