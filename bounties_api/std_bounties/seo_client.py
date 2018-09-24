from bounties import settings
from bounties.sns_client import sns_publish
from bounties.utils import base_url_for, bounty_url_for, profile_url_for
from std_bounties.models import Bounty
from user.models import User
from uuid import uuid4


class SEOClient:

    def __init__(self):
        pass

    def publish_new_sitemap(self, platform):
        if (platform == 'bounties-network' or platform == 'gitcoin') and settings.ENVIRONMENT == 'rinkeby':
            return
        if platform not in PLATFORM_MAPPING and platform != 'gitcoin':
            return
        url = base_url_for(platform)
        domain = url.replace('https://', '')
        base_api_url = 'https://rinkebystaging.api.bounties.network/'
        if settings.ENVIRONMENT == 'rinkeby':
            base_api_url = 'https://rinkebystaging.api.bounties.network/'
        sitemap_url = '{}sitemap.xml?domain={}'.format(base_api_url, domain)
        if url != 'https://explorer.bounties.network':
            sitemap_url = '{}&platform__in={}'.format(sitemap_url, platform)

        sns_publish('sitemap', {'url': sitemap_url, 'bucket': domain})
        sns_publish('ssrcache', {'url': url + '/explorer'})
        sns_publish('ssrcache', {'url': url + '/'})
        sns_publish('ssrcache', {'url': url})

    def clear_cache(self, platform, bounty_id):
        base_url = base_url_for(platform)
        bounty_url = bounty_url_for(bounty_id, platform)
        sns_publish('ssrcache', {'url': bounty_url})

    def bounty_preview_screenshot(self, platform, bounty_id):
        bounty = Bounty.objects.get(bounty_id=bounty_id)
        bounty_url = bounty_url_for(bounty_id, platform)
        image_uuid = uuid4()
        image_path = '{}/bounty_preview/{}-{}.png'.format(settings.ENVIRONMENT, str(bounty_id), image_uuid)
        image_url = 'https://assets.bounties.network/' + image_path
        sns_publish('screenshot', {'url': bounty_url, 'key': image_path})
        bounty.image_preview = image_url
        bounty.save()

    def profile_preview_screenshot(self, user_id):
        user = User.objects.get(id=user_id)
        profile_url = profile_url_for(user.public_address)
        image_uuid = uuid4()
        image_path = '{}/profile_preview/{}-{}.png'.format(settings.ENVIRONMENT, user.public_address, image_uuid)
        image_url = 'https://assets.bounties.network/' + image_path
        user.page_preview = image_url
        user.save()
        sns_publish('screenshot', {'url': profile_url, 'key': image_path})
