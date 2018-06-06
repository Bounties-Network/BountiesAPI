from django.apps import apps
from rest_framework import serializers
from bounties.serializers import CreatableSlugRelatedField
from std_bounties.models import Bounty, Fulfillment, Category, RankedCategory, Token, DraftBounty, Comment
from std_bounties.client_helpers import map_token_data
from std_bounties.constants import STAGE_CHOICES
from django.db import transaction


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


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        field = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('authentication', 'user')
        exclude = ('nonce',)


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
    user = UserSerializer(read_only=True)
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


class DraftBountyWriteSerializer(serializers.ModelSerializer):
    # In general try and not have all this logic in a serializer
    categories = CreatableSlugRelatedField(many=True, slug_field='name', queryset=Category.objects.all())
    tokenContract = serializers.CharField(required=False)
    tokenSymbol = serializers.CharField(read_only=True)
    tokenDecimals = serializers.IntegerField(read_only=True)
    usd_price = serializers.FloatField(read_only=True)
    on_chain = serializers.BooleanField(read_only=True)
    current_market_token_data = TokenSerializer(read_only=True, source='token')
    user = UserSerializer(read_only=True)


    class Meta:
        model = DraftBounty
        exclude = ('identifier', 'calculated_balance', )


    @transaction.atomic
    def create(self, validated_data):
        instance = super(DraftBountyWriteSerializer, self).create(validated_data)
        request = self.context.get('request')
        user = request.current_user
        instance.user = user
        token_data = map_token_data(
            validated_data.get('paysTokens'),
            validated_data.get('tokenContract'),
            validated_data.get('fulfillmentAmount'))
        instance.tokenSymbol = token_data.get('tokenSymbol')
        instance.tokenDecimals = token_data.get('tokenDecimals')
        instance.token = token_data.get('token')
        instance.usd_price = token_data.get('usd_price')
        instance.issuer = 'klsjdflkjsdlf'
        instance.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        updated_instance = super(DraftBountyWriteSerializer, self).update(instance, validated_data)
        token_data = map_token_data(
            instance.paysTokens,
            instance.tokenContract,
            instance.fulfillmentAmount)
        instance.tokenSymbol = token_data.get('tokenSymbol')
        instance.tokenDecimals = token_data.get('tokenDecimals')
        instance.token = token_data.get('token')
        instance.usd_price = token_data.get('usd_price')
        instance.save()
        return instance
