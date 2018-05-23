from rest_framework import serializers
from std_bounties.models import Bounty, Fulfillment, Category, RankedCategory, Token
from std_bounties.constants import STAGE_CHOICES


class CustomSerializer(serializers.ModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(
            CustomSerializer,
            self).get_field_names(
            declared_fields,
            info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class RankedCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = RankedCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BountyFulfillmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bounty
        fields = [
            'id',
            'bounty_id',
            'title',
            'tokenSymbol',
            'tokenDecimals',
            'fulfillmentAmount']


class FulfillmentSerializer(CustomSerializer):
    bounty_data = BountyFulfillmentSerializer(read_only=True, source='bounty')

    class Meta:
        model = Fulfillment
        fields = '__all__'
        extra_kwargs = {
            'data_json': {'write_only': True},
            'data_fulfiller': {'write_only': True},
        }


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class BountySerializer(CustomSerializer):
    bountyStage = serializers.ChoiceField(choices=STAGE_CHOICES)
    categories = CategorySerializer(read_only=True, many=True)
    current_market_token_data = TokenSerializer(read_only=True, source='token')
    fulfillment_count = serializers.ReadOnlyField(source='fulfillments.count')

    class Meta:
        model = Bounty
        fields = '__all__'
        extra_fields = ['id']
        extra_kwargs = {
            'data_categories': {'write_only': True},
            'data_issuer': {'write_only': True},
            'data_json': {'write_only': True},
        }


class LeaderboardFulfillerSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=256)
    name = serializers.CharField(max_length=256)
    email = serializers.CharField(max_length=256)
    githubusername = serializers.CharField(max_length=256)
    total = serializers.DecimalField(decimal_places=0, max_digits=128)
    total_usd = serializers.FloatField()
    bounties_fulfilled = serializers.IntegerField(read_only=True)
    fulfillments_accepted = serializers.IntegerField(read_only=True)


class LeaderboardIssuerSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=256)
    name = serializers.CharField(max_length=256)
    email = serializers.CharField(max_length=256)
    githubusername = serializers.CharField(max_length=256)
    total = serializers.DecimalField(decimal_places=0, max_digits=128)
    total_usd = serializers.FloatField()
    bounties_issued = serializers.IntegerField(read_only=True)
    fulfillments_paid = serializers.IntegerField(read_only=True)
