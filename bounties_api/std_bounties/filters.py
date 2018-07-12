import rest_framework_filters as filters
from std_bounties.models import Bounty, Category, Fulfillment, RankedCategory


class CategoriesFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'normalized_name': ['exact', 'contains', 'startswith', 'endswith', 'in']
        }


class RankedCategoryFilter(filters.FilterSet):
    class Meta:
        model = RankedCategory
        fields = {
            'platform': ['in', 'exact'],
        }


class FulfillmentsFilter(filters.FilterSet):
    class Meta:
        model = Fulfillment
        fields = {
            'fulfiller': ['exact'],
            'bounty': ['exact'],
            'platform': ['exact', 'in'],
        }


class BountiesFilter(filters.FilterSet):
    categories = filters.RelatedFilter(CategoriesFilter, name='categories', queryset=Category.objects.all())
    fulfillments = filters.RelatedFilter(FulfillmentsFilter, name='fulfillments', queryset=Fulfillment.objects.all())
    bounty_created = filters.DateFilter(name='bounty_created')

    class Meta:
        model = Bounty
        fields = {
            'platform': ['in', 'exact'],
            'issuer': ['exact'],
            'fulfillmentAmount': ['exact', 'lt', 'gt', 'lte'],
            'bountyStage': ['exact', 'in'],
            'bounty_created': ['lt', 'gt', 'exact'],
            'deadline': ['lt', 'gt', 'exact'],
            'bounty_id': ['exact'],
        }
