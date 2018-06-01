from rest_framework import serializers

from .models import BountiesTimeline
from drf_queryfields import QueryFieldsMixin
from std_bounties.models import Category, RankedCategory
from std_bounties.serializers import CategorySerializer, RankedCategorySerializer

class BountiesTimelineSerializer(QueryFieldsMixin, serializers.ModelSerializer):

    class Meta:
        model = BountiesTimeline
        fields = "__all__"
        read_only_fields = (
            "bounties_issued",
            "fulfillments_submitted",
            "fulfillments_accepted",
            "fulfillments_pending_acceptance",
            "fulfillment_acceptance_rate",
            "bounty_fulfilled_rate",
            "avg_fulfiller_acceptance_rate",
            "avg_fulfillment_amount",
            "total_fulfillment_amount",
            "bounty_draft",
            "bounty_active",
            "bounty_completed",
            "bounty_expired",
            "bounty_dead",)

class TimelineCategorySerializer(serializers.ModelSerializer):
    total_count = serializers.SerializerMethodField()
    prioritized_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('normalized_name', 'prioritized_name', 'total_count')

    def get_total_count(self, obj):
        return obj.get('total', 0)

    def get_prioritized_name(self, obj):
        try:
            ranked_category = RankedCategory.objects.get(
                normalized_name=obj.get('normalized_name'))
            return ranked_category.name
        except RankedCategory.DoesNotExist:
            return obj.get('normalized_name')
