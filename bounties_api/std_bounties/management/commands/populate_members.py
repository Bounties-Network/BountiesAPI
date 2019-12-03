import requests
from math import pow
from decimal import Decimal
from django.core.management.base import BaseCommand
from std_bounties.models import Community, Bounty, Fulfillment, Membership, Activity
import logging
import sys

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Populate the members table'

    def handle(self, *args, **options):
        try:
            all_activities = Activity.objects.all()
            for activity in all_activities:
                Membership.objects.get_or_create(
                    user_id=activity.user_id,
                    community_id=activity.community_id,
                    defaults={
                        'community_id': activity.community_id,
                        'user_id': activity.user_id,
                        'joined_date': activity.date,
                        'active_member': True
                    },
                )
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
