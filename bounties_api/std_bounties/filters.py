import rest_framework_filters as filters
from std_bounties.models import Bounty, Tag, DraftBounty, Fulfillment, RankedTag, Review


class TagsFilter(filters.FilterSet):
    class Meta:
        model = Tag
        fields = {
            'normalized_name': [
                'exact',
                'contains',
                'startswith',
                'endswith',
                'in']}


class RankedTagFilter(filters.FilterSet):
    class Meta:
        model = RankedTag
        fields = {
            'platform': ['exact'],
        }


class ReviewsFilter(filters.FilterSet):
    class Meta:
        model = Review
        fields = {
            'reviewer__public_address': ['exact'],
            'reviewee__public_address': ['exact'],
            'platform': ['exact', 'in'],
        }


class FulfillmentsFilter(filters.FilterSet):
    class Meta:
        model = Fulfillment
        fields = {
            'fulfillment_id': ['exact'],
            'fulfiller': ['exact'],
            'bounty': ['exact'],
            'bounty__user__public_address': ['exact'],
            'platform': ['exact', 'in'],
        }


class DraftBountiesFilter(filters.FilterSet):
    class Meta:
        model = DraftBounty
        fields = {
            'issuer': ['exact'],
            'platform': ['in', 'exact'],
        }


class BountiesFilter(filters.FilterSet):
    tags = filters.RelatedFilter(
        TagsFilter,
        name='tags',
        queryset=Tag.objects.all())
    fulfillments = filters.RelatedFilter(
        FulfillmentsFilter,
        name='fulfillments',
        queryset=Fulfillment.objects.all())
    bounty_created = filters.DateFilter(name='bounty_created')

    class Meta:
        model = Bounty
        fields = {
            'platform': ['in', 'exact'],
            'issuer': ['exact'],
            'experienceLevel': ['exact', 'in'],
            'fulfillmentAmount': ['exact', 'lt', 'gt', 'lte'],
            'bountyStage': ['exact', 'in'],
            'bounty_created': ['lt', 'gt', 'exact'],
            'deadline': ['lt', 'gt', 'exact'],
            'bounty_id': ['exact'],
        }
