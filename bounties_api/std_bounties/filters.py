import django_filters
from django_filters import CharFilter, BaseInFilter
from std_bounties.models import Bounty

class CharInFilter(BaseInFilter, CharFilter):
    pass

class CategoriesFilter(django_filters.FilterSet):
    has_categories = CharInFilter(name='categories__normalized_name', lookup_expr='in')
    issuer__ne = CharFilter(name='issuer', exclude=True)

    class Meta:
        model = Bounty
        fields = ['issuer', 'fulfillmentAmount', 'bountyStage', 'has_categories', 'issuer__ne']
