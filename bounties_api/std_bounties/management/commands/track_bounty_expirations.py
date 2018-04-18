import time
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from std_bounties.constants import ACTIVE_STAGE, EXPIRED_STAGE
from std_bounties.models import Bounty
import logging

logger = logging.getLogger('django')

# TODO - This should just be a scheduled cronjob.
# There is no need to have this as a long running job


class Command(BaseCommand):
    help = 'Listen for contract events'

    def handle(self, *args, **options):
        try:
            while True:
                expired_bounties = Bounty.objects.filter(
                    deadline__lt=datetime.now(timezone.utc),
                    bountyStage=ACTIVE_STAGE
                )
                for bounty in expired_bounties:
                    bounty.bountyStage=EXPIRED_STAGE
                    bounty.save()
                    bounty.record_bounty_state(bounty.deadline)
                time.sleep(60)
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
