from rest_framework import serializers
from std_bounties.models import Bounty, Fulfillment, Category, RankedCategory, Token
from std_bounties.constants import STAGE_CHOICES


class ChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj][1]


class RankedCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RankedCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class FulfillmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fulfillment
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'

class BountySerializer(serializers.ModelSerializer):
    bountyStage = ChoicesField(choices=STAGE_CHOICES)
    categories = CategorySerializer(read_only=True, many=True)
    current_market_token_data = TokenSerializer(read_only=True, source='token')
    fulfillment_count = serializers.ReadOnlyField(source='fulfillment_set.count')

    class Meta:
        model = Bounty
        fields = '__all__'


