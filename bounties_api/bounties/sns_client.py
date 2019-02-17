import boto3
import json
from botocore.exceptions import ClientError
import logging
from django.conf import settings


logger = logging.getLogger('django')


AWS_REGION = 'us-east-1'
client = boto3.client('sns', region_name=AWS_REGION)


def sns_publish(receiver, message):
    if settings.LOCAL:
        return
    if settings.ENVIRONMENT not in ['production', 'rinkeby']:
        return
    try:
        print('Target ARN for publish {}:{}'.format(settings.SNS_ADDRESS, receiver))
        client.publish(TargetArn='{}:{}'.format(settings.SNS_ADDRESS, receiver), Message=json.dumps(message))
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
