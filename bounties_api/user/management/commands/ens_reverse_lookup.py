import logging
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from user.models import User
from web3 import Web3, HTTPProvider
from ens import ENS
from django.conf import settings

web3 = Web3(HTTPProvider(settings.NETWORKS['mainNet']))

ns = ENS.fromWeb3(web3)
logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Script to find ens domains for users'

    def handle(self, *args, **options):
        try:
            last_date = datetime.utcnow() - timedelta(days=1)
            users = User.objects.all().filter(
                last_logged_in__gte=last_date
            )
            for user in users:
                public_address = Web3.toChecksumAddress(user.public_address)
                domain = ns.name(public_address)
                if domain is not None:
                    parts = domain.split('.')
                    if len(parts) == 2 and parts[1] == 'eth':
                        user.ens_domain = domain
                        user.save()

        except Exception as e:
            logger.exception(e)
            raise e
