from rest_framework import serializers

from .models import BountiesTimeline, Tokens
from drf_queryfields import QueryFieldsMixin
from std_bounties.models import Category


class BountiesTimelineSerializer(
        QueryFieldsMixin,
        serializers.ModelSerializer):
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
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'normalized_name', 'total_count')

    def get_total_count(self, obj):
        return obj.get('total', 0)

    def get_name(self, obj):
        ranked_categories = self.context.get('ranked_categories', {})
        normalized_name = obj.get('normalized_name')
        name = ranked_categories.get(normalized_name, normalized_name)
        return name


class TokenListSerializer(serializers.ModelSerializer):
    token_symbol = serializers.SerializerMethodField()
    token_contract = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()
    price_usd = serializers.SerializerMethodField()

    class Meta:
        model = Tokens
        fields = ('token_symbol', 'token_contract', 'total_count', 'price_usd')

    def get_total_count(self, obj):
        return obj.get('count', 0)

    def get_token_symbol(self, obj):
        return obj.get('tokenSymbol')

    def get_token_contract(self, obj):
        return obj.get('tokenContract')

    def get_price_usd(self, obj):
        token_array = obj.get('token')
        if len(token_array) == 0:
            return 0
        else:
            token_attributes = token_array[0]
            return token_attributes.get('price_usd')
