from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend
from std_bounties.models import Contract
from std_bounties.serializers import ContractSerializer
from std_bounties.filters import ContractFilter


class ContractViewSet(ReadOnlyModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    filter_class = ContractFilter
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = (
        'contract_version',
        'contract_address',
        'contract_type',
    )
