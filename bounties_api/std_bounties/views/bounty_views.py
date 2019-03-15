from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend
from std_bounties.serializers import BountySerializer
from std_bounties.models import Bounty
from std_bounties.filters import BountiesFilter


class MultipleFieldLookupMixin(object):

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object


class BountyViewSet(MultipleFieldLookupMixin, ReadOnlyModelViewSet):
    serializer_class = BountySerializer
    queryset = Bounty.objects.all().prefetch_related('categories').select_related('token').distinct()
    filter_class = BountiesFilter
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    ordering_fields = (
        'fulfillmentAmount',
        'deadline',
        'bounty_created',
        'usd_price'
    )
    search_fields = (
        'title',
        'description',
        'categories__normalized_name',
        'issuer'
    )
    lookup_fields = ('bounty_id', 'contract_version')
