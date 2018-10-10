import requests
import boto3
from random import random
from django.core.management.base import BaseCommand
from django.db.models import Q, Count
from botocore.exceptions import ClientError
from user.models import User
from django.conf import settings
from std_bounties.seo_client import SEOClient
import logging


seo_client = SEOClient()


AWS_REGION = 'us-east-1'
client = boto3.client('s3', region_name=AWS_REGION)
logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Script to get user data from github - should run daily'

    def handle(self, *args, **options):
        try:
            users = User.objects.all().exclude(
                Q(github='') |
                Q(profile_touched_manually=True)
            ).filter(
                large_profile_image_url=''
            )

            for user in users:
                url = 'https://api.github.com/users/{}'.format(user.github)
                response = requests.get(url, headers={'Authorization': 'token ' + settings.GITHUB_TOKEN})

                if response.status_code != 200:
                    continue

                github_data = response.json()

                large_image_url = github_data.get('avatar_url') + '&s=300'
                small_image_url = github_data.get('avatar_url') + '&s=64'

                large_image_response = requests.get(large_image_url)
                small_image_response = requests.get(small_image_url)

                if large_image_response.status_code == 200 and small_image_response.status_code == 200:
                    try:
                        nonce = int(random() * 1000)
                        bucket = 'assets.bounties.network'

                        small_key = '{}/userimages/{}-sm-{}.png'.format(settings.ENVIRONMENT, user.public_address, nonce)
                        large_key = '{}/userimages/{}-lg-{}.png'.format(settings.ENVIRONMENT, user.public_address, nonce)

                        client.put_object(
                            Body=small_image_response.content,
                            ContentType=small_image_response.headers['content-type'],
                            CacheControl='max-age=31536000',
                            Bucket=bucket,
                            ACL='public-read',
                            Key=small_key)

                        client.put_object(
                            Body=large_image_response.content,
                            ContentType=large_image_response.headers['content-type'],
                            CacheControl='max-age=31536000',
                            Bucket=bucket,
                            ACL='public-read',
                            Key=large_key)

                        user.small_profile_image_url = 'https://{}/{}'.format(bucket, small_key)
                        user.large_profile_image_url = 'https://{}/{}'.format(bucket, large_key)

                        user.save()

                        logger.info('uploaded for: {}'.format(user.public_address))
                    except ClientError as e:
                        logger.error(e.response['Error']['Message'])

            users_for_screenshots = User.objects.annotate(bounty_count=Count('bounty')).annotate(fulfillment_count=Count('fulfillment')).filter(Q(bounty_count__gt=0) | Q(fulfillment_count__gt=0) | Q(large_profile_image_url__gt='')).filter(page_preview='')
            for user in users_for_screenshots:
                seo_client.profile_preview_screenshot(user.id)
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
