from std_bounties.models import Bounty
from std_bounties.seo_client import SEOClient
from django.core.management.base import BaseCommand


seo_client = SEOClient()


class Command(BaseCommand):
    help = 'Initiate bounty screenshots'

    def handle(self, *args, **options):
        bounties = Bounty.objects.all()
        for bounty in bounties:
            seo_client.bounty_preview_screenshot(bounty.platform, bounty.id)
