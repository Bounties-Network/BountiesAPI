from django.apps import apps
from django.db import transaction
from rest_framework import serializers

from bounties.serializers import CreatableSlugRelatedField
from std_bounties.models import (
    Bounty,
    Fulfillment,
    Tag,
    RankedTag,
    Token,
    DraftBounty,
    Comment,
    Review
)
from std_bounties.client_helpers import map_token_data
from std_bounties.constants import STAGE_CHOICES
from notifications.notification_client import NotificationClient

notification_client = NotificationClient()


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


class RankedTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = RankedTag
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('user', 'user')
        exclude = ('nonce', 'settings', 'profile_touched_manually',)


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewee = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.current_user
        updated_data = {
            **validated_data,
            'user': user,
        }
        return Comment.objects.create(**updated_data)


class BountyFulfillmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Bounty
        fields = [
            'id',
            'bounty_id',
            'bountyStage',
            'title',
            'usd_price',
            'tokenSymbol',
            'tokenDecimals',
            'fulfillmentAmount',
            'calculated_fulfillmentAmount',
            'user']


class FulfillmentSerializer(CustomSerializer):
    bounty_data = BountyFulfillmentSerializer(read_only=True, source='bounty')
    fulfiller_review = ReviewSerializer(read_only=True)
    issuer_review = ReviewSerializer(read_only=True)
    user = UserSerializer(read_only=True)

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
    tags = TagSerializer(read_only=True, many=True)
    current_market_token_data = TokenSerializer(read_only=True, source='token')
    user = UserSerializer(read_only=True)
    fulfillment_count = serializers.ReadOnlyField(source='fulfillments.count')
    comment_count = serializers.ReadOnlyField(source='comments.count')

    class Meta:
        model = Bounty
        exclude = ('comments',)
        extra_fields = ['id']
        extra_kwargs = {
            'data_tags': {'write_only': True},
            'data_issuer': {'write_only': True},
            'data_json': {'write_only': True},
        }


class LeaderboardFulfillerSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=256)
    name = serializers.CharField(max_length=256)
    email = serializers.CharField(max_length=256)
    githubusername = serializers.CharField(max_length=256)
    profile_image = serializers.CharField(max_length=256)
    total = serializers.DecimalField(decimal_places=0, max_digits=128)
    total_usd = serializers.FloatField()
    bounties_fulfilled = serializers.IntegerField(read_only=True)
    fulfillments_accepted = serializers.IntegerField(read_only=True)


class LeaderboardIssuerSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=256)
    name = serializers.CharField(max_length=256)
    email = serializers.CharField(max_length=256)
    githubusername = serializers.CharField(max_length=256)
    profile_image = serializers.CharField(max_length=256)
    total = serializers.DecimalField(decimal_places=0, max_digits=128)
    total_usd = serializers.FloatField()
    bounties_issued = serializers.IntegerField(read_only=True)
    fulfillments_paid = serializers.IntegerField(read_only=True)


class DraftBountyWriteSerializer(serializers.ModelSerializer):
    # In general try and not have all this logic in a serializer
    tags = CreatableSlugRelatedField(
        many=True, slug_field='name', queryset=Tag.objects.all())
    tokenContract = serializers.CharField(required=False, allow_blank=True)
    tokenSymbol = serializers.CharField(read_only=True)
    tokenDecimals = serializers.IntegerField(read_only=True)
    arbiter = serializers.CharField(allow_blank=True, required=False)
    usd_price = serializers.FloatField(read_only=True)
    on_chain = serializers.BooleanField(read_only=True)
    current_market_token_data = TokenSerializer(read_only=True, source='token')
    webReferenceURL = serializers.CharField(required=False, allow_blank=True)
    uid = serializers.CharField(read_only=True)
    calculated_fulfillmentAmount = serializers.DecimalField(
        decimal_places=30,
        max_digits=70,
        read_only=True)
    user = UserSerializer(read_only=True)
    issuer = serializers.CharField(read_only=True)

    class Meta:
        model = DraftBounty
        exclude = ('token',)

    @transaction.atomic
    def create(self, validated_data):
        instance = super(
            DraftBountyWriteSerializer,
            self).create(validated_data)
        request = self.context.get('request')
        user = request.current_user
        instance.user = user
        token_data = map_token_data(
            validated_data.get('paysTokens'),
            validated_data.get('tokenContract'),
            validated_data.get('fulfillmentAmount'))
        instance.tokenSymbol = token_data.get('tokenSymbol')
        instance.tokenDecimals = token_data.get('tokenDecimals')
        instance.token_id = token_data.get('token')
        instance.usd_price = token_data.get('usd_price')
        instance.issuer = user.public_address
        instance.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        super(
            DraftBountyWriteSerializer,
            self).update(
            instance,
            validated_data)
        token_data = map_token_data(
            instance.paysTokens,
            instance.tokenContract,
            instance.fulfillmentAmount)
        instance.tokenSymbol = token_data.get('tokenSymbol')
        instance.tokenDecimals = token_data.get('tokenDecimals')
        instance.token_id = token_data.get('token')
        instance.usd_price = token_data.get('usd_price')
        instance.save()
        return instance
