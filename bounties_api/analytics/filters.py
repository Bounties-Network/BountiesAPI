from django_filters.rest_framework import FilterSet
from django_filters import rest_framework as filters

from analytics.models import BountiesTimeline


class BountiesTimelineFilter(FilterSet):
    since = filters.DateFilter(name="date", lookup_expr='gte')
    until = filters.DateFilter(name="date", lookup_expr='lte')

    class Meta:
        model = BountiesTimeline
        fields = {'since': ['date__gte'],
                  'until': ['date__lte'],
                  'is_week': ['exact'],
                  'bounties_issued_cum': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'bounties_issued': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'fulfillments_submitted_cum': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'fulfillments_submitted': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'fulfillments_accepted_cum': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'fulfillments_accepted': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'fulfillments_pending_acceptance': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'fulfillment_acceptance_rate': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'bounty_fulfilled_rate': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'avg_fulfiller_acceptance_rate': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'avg_fulfillment_amount': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'total_fulfillment_amount': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'bounty_draft': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'bounty_active': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'bounty_completed': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'bounty_expired': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'bounty_dead': ['gt', 'gte', 'lt', 'lte', 'exact'],
                  'schema': ['exact']
        }
