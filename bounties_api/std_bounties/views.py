from rest_framework import viewsets
from std_bounties.models import Bounty, Fulfillment
from std_bounties.serializers import BountySerializer, FulfillmentSerializer

class BountyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = BountySerializer
    queryset = Bounty.objects.all()

class FulfillmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FulfillmentSerializer
    queryset = Fulfillment.objects.all()
