import requests
from math import pow
from decimal import Decimal
from django.core.management.base import BaseCommand
from std_bounties.models import Activity, Community, Bounty, Event, Comment, Fulfillment, FulfillerApplication
import logging
import sys

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Populate the activities table with applications'

    def handle(self, *args, **options):
        try:
            all_applications = FulfillerApplication.objects.all()
            for application in all_applications:
                bounty = Bounty.objects.get(id=application.bounty_id)
                Activity.objects.create(
                    event_type='ApplicationCreated',
                    bounty_id=bounty.id,
                    date=application.created,
                    user_id=application.applicant_id,
                    community_id=bounty.community_id)
                if application.state == 'A':
                    Activity.objects.create(
                        event_type='ApplicationAccepted',
                        bounty_id=bounty.id,
                        date=application.modified,
                        user_id=bounty.user_id,
                        community_id=bounty.community_id)
                elif application.state == 'R':
                    Activity.objects.create(
                        event_type='ApplicationRejected',
                        bounty_id=bounty.id,
                        date=application.modified,
                        user_id=bounty.user_id,
                        community_id=bounty.community_id)
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            sys.exit(1)
