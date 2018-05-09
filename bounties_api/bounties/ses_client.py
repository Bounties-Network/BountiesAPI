import boto3
from botocore.exceptions import ClientError
import logging
from django.conf import settings


logger = logging.getLogger('django')


SENDER = 'Bounties Team <team@bounties.network>'
AWS_REGION = 'us-east-1'
CHARSET = "UTF-8"
client = boto3.client('ses', region_name=AWS_REGION,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID)

def send_email(receiver, subject, text):
    if settings.LOCAL:
        return
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    receiver,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
    else:
        logger.info('email sent to {}'.format(receiver))

