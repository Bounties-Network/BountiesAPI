from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend
from std_bounties.serializers import BountySerializer
from std_bounties.models import Bounty
from std_bounties.filters import BountiesFilter


class BountyViewSet(ReadOnlyModelViewSet):
    serializer_class = BountySerializer
    queryset = Bounty.objects.all().prefetch_related('categories').select_related('token').distinct()
    filter_class = BountiesFilter
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    ordering_fields = (
        'fulfillment_amount',
        'deadline',
        'bounty_created',
        'usd_price',
        'view_count'
    )
    search_fields = (
        'title',
        'description',
        'categories__normalized_name',
        'issuer',
        'contract_version',
        'community_id'
    )
