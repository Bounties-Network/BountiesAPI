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
                Q(github=''), Q(large_profile_image_url='')
            )

            for user in users:
                image_r = None

                if user.github and not user.profile_touched_manually and not user.profile_image:
                    github_username = user.github
                    if not github_username:
                        continue
                    url = 'https://api.github.com/users/{}'.format(github_username)
                    r = requests.get(
                        url, headers={
                            'Authorization': 'token ' + settings.GITHUB_TOKEN})

                    if r.status_code == 200:
                        github_data = r.json()
                        github_image = github_data.get('avatar_url')
                        image_r = requests.get(github_image)

                if image_r and image_r.status_code == 200:
                    try:
                        nonce = int(random() * 1000)
                        bucket = 'assets.bounties.network'
                        key = '{}/userimages/{}-{}.jpg'.format(
                            settings.ENVIRONMENT, user.public_address, nonce)

                        client.put_object(
                            Body=image_r.content,
                            ContentType=image_r.headers['content-type'],
                            Bucket=bucket,
                            ACL='public-read',
                            Key=key)

                        user.small_profile_image_url = 'https://{}/{}'.format(bucket, key)
                        user.large_profile_image_url = 'https://{}/{}'.format(bucket, key)

                        user.save()

                        logger.info('uploaded for: {}'.format(user.public_address))
                    except ClientError as e:
                        logger.error(e.response['Error']['Message'])

            users_for_screenshots = User.objects.annotate(bounty_count=Count('bounty')).annotate(fulfillment_count=Count('fulfillment')).filter(Q(bounty_count__gt=0) | Q(fulfillment_count__gt=0) | Q(profile_image__gt='')).filter(page_preview='')
            for user in users_for_screenshots:
                seo_client.profile_preview_screenshot(user.id)
        except Exception as e:
            # goes to rollbar
            logger.exception(e)
            raise e
