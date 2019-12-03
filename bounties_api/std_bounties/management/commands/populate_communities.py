import requests
from math import pow
from decimal import Decimal
from django.core.management.base import BaseCommand
from std_bounties.models import Community, Bounty, Fulfillment
import logging
import sys

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Populate the communities table'

    def handle(self, *args, **options):
        try:
            all_bounties = Bounty.objects.all()
            for bounty in all_bounties:
                platform = bounty.platform
                community, created = Community.objects.get_or_create(
                    community_id=str(platform),
                    defaults={
                        'community_id': platform,
                        'community_name': platform,
                        'created': bounty.created,
                        'modified': bounty.created,
                        'public': True,
                        'network': bounty.network,
                        'admin_user_id': 1
                    },
                )
                bounty.community = community
                bounty.save()
            all_fulfillments = Fulfillment.objects.all()
            for fulfillment in all_fulfillments:
                platform = fulfillment.platform
                community, created = Community.objects.get_or_create(
                    community_id=str(platform),
                    defaults={
                        'community_id': platform,
                        'community_name': platform,
                        'created': fulfillment.created,
                        'modified': fulfillment.created,
                        'public': True,
                        'network': fulfillment.network,
                        'admin_user_id': 1
                    },
                )
                fulfillment.community = community
                fulfillment.save()
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
