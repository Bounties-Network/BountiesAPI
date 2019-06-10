from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework_filters.backends import DjangoFilterBackend
from std_bounties.models import RankedCategory
from std_bounties.serializers import RankedCategorySerializer
from std_bounties.filters import RankedCategoryFilter


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = RankedCategorySerializer
    queryset = RankedCategory.objects.all()
    filter_class = RankedCategoryFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    ordering_fields = ('total_count',)
    ordering = ('-total_count',)
    search_fields = ('normalized_name',)
