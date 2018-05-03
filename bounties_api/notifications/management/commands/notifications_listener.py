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
                # poll by the second
                if not settings.LOCAL:
                    time.sleep(1)

                response = sqs_client.receive_message(
                    QueueUrl=settings.NOTIFICATIONS_URL,
                    AttributeNames=['MessageDeduplicationId'],
                    MessageAttributeNames=['All'],
                )

                messages = response.get('Messages')

                if not messages:
                    continue

                message = messages[0]

                receipt_handle = message['ReceiptHandle']
                message_attributes = message['MessageAttributes']

                user_id = int(message_attributes['UserId']['StringValue'])
                time_stamp = int(message_attributes['TimeStamp']['StringValue'])
                notification_id = int(message_attributes['NotificationId']['StringValue'])
                data = json.loads(message_attributes['Data']['StringValue'])

        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
