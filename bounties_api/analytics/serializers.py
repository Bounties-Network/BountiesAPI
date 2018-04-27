from rest_framework import serializers

from .models import BountiesTimeline


class BountiesTimelineSerializer(serializers.ModelSerializer):
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
