import boto3
from botocore.exceptions import ClientError
import logging
from django.conf import settings


logger = logging.getLogger('django')


SENDER = 'Bounties Team <team@bounties.network>'
AWS_REGION = 'us-east-1'
CHARSET = 'UTF-8'
client = boto3.client('ses', region_name=AWS_REGION)


def send_email(receiver, subject, html):
    if settings.LOCAL:
        return
    if settings.ENVIRONMENT not in ['production', 'consensys', 'rinkstaging', 'staging', 'rinkeby']:
        return
    try:
        client.send_email(
            Destination={
                'ToAddresses': [
                    receiver,
                ],
            },
            Message={
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': html,
                    },
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
    else:
        logger.info('email sent to {}'.format(receiver))
