from rest_framework import viewsets
from std_bounties.models import Bounty, Fulfillment
from std_bounties.serializers import BountySerializer, FulfillmentSerializer

class BountyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = BountySerializer
    queryset = Bounty.objects.all()
    filter_fields = ('deadline', 'issuer', 'fulfillmentAmount', 'bountyStage', 'bounty_created')
    ordering_fields = ('fulfillmentAmount', 'deadline', 'bounty_created')

class FulfillmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FulfillmentSerializer
    queryset = Fulfillment.objects.all()
