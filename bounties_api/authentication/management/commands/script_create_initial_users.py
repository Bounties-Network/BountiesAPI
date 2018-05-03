from django.core.management.base import BaseCommand
from authentication.models import User
from std_bounties.models import Bounty, Fulfillment


import logging
logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Script to Create the Users From Current Bounties and Fulfillments'

    def handle(self, *args, **options):
        try:
            bounties = Bounty.objects.all()
            for bounty in bounties:
                
            fulfillments = Fulfillment.objects.all()
            for fulfillment in fulfillments:

        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
