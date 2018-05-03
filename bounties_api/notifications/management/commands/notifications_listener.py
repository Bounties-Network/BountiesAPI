from django.core.management.base import BaseCommand

from django.conf import settings
from bounties.sqs_client import sqs_client
import logging


logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Listen to SQS queue for notifications to create'

    def handle(self, *args, **options):
        try:
            while True:
                # logic here
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
