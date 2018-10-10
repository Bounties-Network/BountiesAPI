import logging
import requests
import boto3
from random import random
from django.core.management.base import BaseCommand
from django.db.models import Q
from botocore.exceptions import ClientError
from user.models import User
from django.conf import settings
from PIL import Image
from io import BytesIO


SMALL_IMAGE_SIZE = 64, 64
AWS_REGION = 'us-east-1'
client = boto3.client('s3', region_name=AWS_REGION)
logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Script to resize all large profile images and reupload to S3.'

    def handle(self, *args, **options):
        try:
            users = User.objects.all().exclude(large_profile_image_url='').filter(
                Q(small_profile_image_url__isnull=True) |
                Q(small_profile_image_url__exact='')
            )

            for user in users:
                response = requests.get(user.large_profile_image_url)

                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    image.thumbnail(SMALL_IMAGE_SIZE)

                    resized_image_content = BytesIO()
                    image.save(resized_image_content, format='PNG')

                    nonce = int(random() * 1000)
                    bucket = 'assets.bounties.network'
                    key = '{}/userimages/{}-{}.jpg'.format(settings.ENVIRONMENT, user.public_address, nonce)

                    try:
                        client.put_object(
                            Body=resized_image_content.getvalue(),
                            ContentType=response.headers['content-type'],
                            CacheControl=response.headers['cache-control'],
                            ContentDisposition=response.headers['content-disposition'],
                            Bucket=bucket,
                            ACL='public-read',
                            Key=key)

                        user.small_profile_image_url = 'https://{}/{}'.format(bucket, key)

                        user.save()

                        logger.info('uploaded resize profile image for: {}'.format(user.public_address))
                    except ClientError as e:
                        logger.error(e.response['Error']['Message'])
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
