from rest_framework import serializers

from .models import BountiesTimeline


class BountiesTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BountiesTimeline
        read_only_fields = '__all__'
