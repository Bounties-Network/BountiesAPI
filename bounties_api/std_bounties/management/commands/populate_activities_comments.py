import requests
from math import pow
from decimal import Decimal
from django.core.management.base import BaseCommand
from std_bounties.models import Activity, Community, Bounty, Event, Comment, FulfillerApplication
import logging
import sys

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Populate the activities table with comments'

    def handle(self, *args, **options):
        try:
            all_comments = Comment.objects.all()
            for comment in all_comments:
                bounty = Bounty.objects.filter(comment = comment)
                fulfillment = Fulfillment.objects.filter(comment = comment)
                print('got bounty')
                print(bounty)
                print('got ful')
                print(ful)

        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
