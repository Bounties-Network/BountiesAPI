from rest_framework import serializers
from std_bounties.models import Bounty, Fulfillment, Category
from std_bounties.constants import STAGE_CHOICES


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class BountySerializer(serializers.ModelSerializer):
    bountyStage = serializers.ChoiceField(choices=STAGE_CHOICES)
    categories = CategorySerializer(read_only=True, many=True)
    fulfillment_count = serializers.ReadOnlyField(source='fulfillment_set.count')

    class Meta:
        model = Bounty
        fields = '__all__'


class FulfillmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fulfillment
        fields = '__all__'
