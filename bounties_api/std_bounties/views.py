from rest_framework import viewsets
from std_bounties.models import Bounty, Fulfillment
from std_bounties.serializers import BountySerializer, FulfillmentSerializer
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
