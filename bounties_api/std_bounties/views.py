from rest_framework import viewsets
from std_bounties.models import Bounty, Fulfillment, RankedCategory
from std_bounties.serializers import BountySerializer, FulfillmentSerializer, RankedCategorySerializer
from std_bounties.filters import BountiesFilter, FulfillmentsFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend


class BountyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = BountySerializer
    queryset = Bounty.objects.all()
    filter_class = BountiesFilter
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('fulfillmentAmount', 'deadline', 'bounty_created')
    search_fields = ('title', 'description', 'categories__normalized_name')

class FulfillmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FulfillmentSerializer
    queryset = Fulfillment.objects.all()
    filter_class = FulfillmentsFilter
    filter_backends = (DjangoFilterBackend,)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = RankedCategorySerializer
    queryset = RankedCategory.objects.all()
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('total_count',)
    ordering = ('-total_count',)
    search_fields = ('normalized_name',)
