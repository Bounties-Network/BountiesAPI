from django.core.management.base import BaseCommand
from authentication.models import User
from std_bounties.models import Bounty, Fulfillment


import logging
logger = logging.getLogger('django')


class Command(BaseCommand):
    # This is a temp script/migration script - not something that runs regularly
    help = 'Script to Create the Users From Current Bounties and Fulfillments'

    def handle(self, *args, **options):
        try:
            bounties = Bounty.objects.all()

            for bounty in bounties:
                name = bounty.issuer_name
                email = bounty.issuer_email
                public_address = bounty.issuer_address
                # Update to make the create/update logic only based on address
                user, updated = User.objects.update_or_create(
                    public_address=public_address,
                    defaults={
                        "name": name,
                        "email": email,
                    }
                )
                bounty.user = user
                bounty.save()

            fulfillments = Fulfillment.objects.all()

            for fulfillment in fulfillments:
                name = fulfillment.fulfiller_name
                email = fulfillment.fulfiller_email
                public_address = fulfillment.fulfiller_address
                # Update to make the create/update logic only based on address
                user, updated = User.objects.update_or_create(
                    public_address=public_address,
                    defaults={
                        "name": name,
                        "email": email,
                    }
                )
                fulfillment.user = user
                fulfillment.save()
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
