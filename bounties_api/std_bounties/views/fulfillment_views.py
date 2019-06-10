from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework_filters.backends import DjangoFilterBackend
from django.db.models import Q
from std_bounties.serializers import FulfillmentSerializer
from std_bounties.models import Fulfillment
from std_bounties.filters import FulfillmentsFilter


class FulfillmentViewSet(ReadOnlyModelViewSet):
    serializer_class = FulfillmentSerializer
    queryset = Fulfillment.objects.all().select_related('bounty')

    def get_queryset(self):
        qs = Fulfillment.objects.all().select_related('bounty')

        current_user = self.request.current_user

        if current_user:
            return qs.filter(
                Q(fulfiller=current_user.public_address) |
                Q(bounty__issuer=current_user.public_address) |
                Q(bounty__private_fulfillments=False)
            )
        else:
            return Fulfillment.objects.filter(bounty__private_fulfillments=False)

    filter_class = FulfillmentsFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = (
        'fulfillment_created',
        'usd_price'
    )
