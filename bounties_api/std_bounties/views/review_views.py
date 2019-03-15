from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework_filters.backends import DjangoFilterBackend
from std_bounties.models import Review
from std_bounties.serializers import ReviewSerializer
from std_bounties.filters import ReviewsFilter


class ReviewsViewSet(ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        review_type = self.request.GET.get('review_type', '')

        if review_type == 'fulfiller':
            return Review.objects.filter(fulfillment_review__isnull=False)
        if review_type == 'issuer':
            return Review.objects.filter(issuer_review__isnull=False)
        return Review.objects.all()

    filter_class = ReviewsFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend,)

    ordering_fields = (
        'created',
        'rating')
