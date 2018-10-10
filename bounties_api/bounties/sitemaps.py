from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from std_bounties.models import Bounty
from user.models import User
from django.db.models import Q
from django.db.models import Count
from std_bounties.constants import DRAFT_STAGE, ACTIVE_STAGE, DEAD_STAGE, COMPLETED_STAGE, EXPIRED_STAGE


class SiteMapDomainMixin(Sitemap):
    protocol = 'https'

    def get_urls(self, page=1, site=None, protocol=None):
        site = Site(domain=self.domain, name=self.domain)
        return super(
            SiteMapDomainMixin,
            self).get_urls(
            page,
            site,
            protocol=None)


class BountyMap(SiteMapDomainMixin):
    def __init__(self, platform_filters, domain):
        current_filters = {}
        if platform_filters:
            current_filters['platform__in'] = platform_filters
        self.platform_filter = current_filters
        self.domain = domain
        super().__init__()

    def items(self):
        return Bounty.objects.filter(
            **self.platform_filter).exclude(bountyStage=DRAFT_STAGE).order_by('-modified')

    def priority(self, obj):
        if obj.bountyStage == ACTIVE_STAGE:
            return 1
        if obj.bountyStage == DEAD_STAGE:
            return .5
        if obj.bountyStage == COMPLETED_STAGE:
            return .75
        if obj.bountyStage == EXPIRED_STAGE:
            return .5

    def changefreq(self, obj):
        if obj.bountyStage == ACTIVE_STAGE:
            return 'hourly'
        if obj.bountyStage == DEAD_STAGE:
            return 'daily'
        if obj.bountyStage == COMPLETED_STAGE:
            return 'daily'
        if obj.bountyStage == EXPIRED_STAGE:
            return 'daily'

    def lastmod(self, obj):
        return obj.modified

    def location(self, obj):
        return '/bounty/' + str(obj.bounty_id)


class ProfileMap(SiteMapDomainMixin):
    def __init__(self, platform_filters, domain):
        current_filters = {}
        if platform_filters:
            current_filters['bounty__platform__in'] = platform_filters
        self.domain = domain
        self.platform_filter = current_filters
        super().__init__()

    changefreq = 'weekly'
    priority = .1

    def items(self):
        return User.objects.filter(
            **self.platform_filter).annotate(
            bounty_count=Count('bounty')).annotate(
            fulfillment_count=Count('fulfillment')).filter(
                Q(
                    bounty_count__gt=0) | Q(
                        fulfillment_count__gt=0) | Q(
                            small_profile_image_url__gt=''))

    def location(self, obj):
        return '/profile/' + obj.public_address


class StaticMap(SiteMapDomainMixin):
    def __init__(self, platform_filters, domain):
        self.platform_filter = platform_filters
        self.domain = domain
        super().__init__()

    def items(self):
        return ['explorer', 'leaderboard', 'main']

    def priority(self, obj):
        if obj == 'explorer':
            priority = 1
        if obj == 'leaderboard':
            priority = .75
        if obj == 'main':
            priority = 1
        return priority

    def changefreq(self, obj):
        if obj == 'explorer':
            frequency = 'always'
        if obj == 'leaderboard':
            frequency = 'daily'
        if obj == 'main':
            frequency = 'always'
        return frequency

    def location(self, obj):
        if obj == 'main':
            return ''
        return '/' + obj
