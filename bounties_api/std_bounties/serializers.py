from django.apps import apps
from django.db import transaction
from rest_framework import serializers

from bounties.serializers import CreatableSlugRelatedField
from std_bounties.models import (
    Bounty,
    Contribution,
    Fulfillment,
    FulfillerApplication,
    Category,
    RankedCategory,
    Token,
    DraftBounty,
    Comment,
    Review,
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


class RankedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RankedCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
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
            'bounty_stage',
            'title',
            'usd_price',
            'token_symbol',
            'token_decimals',
            'fulfillment_amount',
            'calculated_fulfillment_amount',
            'user'
        ]


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = '__all__'


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
    bounty_stage = serializers.ChoiceField(choices=STAGE_CHOICES)
    categories = CategorySerializer(read_only=True, many=True)
    current_market_token_data = TokenSerializer(read_only=True, source='token')
    user = UserSerializer(read_only=True)
    fulfillment_count = serializers.ReadOnlyField(source='fulfillments.count')
    application_count = serializers.SerializerMethodField()
    comment_count = serializers.ReadOnlyField(source='comments.count')

    class Meta:
        model = Bounty
        exclude = ('comments',)
        extra_fields = ['id']
        extra_kwargs = {
            'data_categories': {'write_only': True},
            'data_issuer': {'write_only': True},
            'data_json': {'write_only': True},
        }

    def get_application_count(self, obj):
        return obj.fulfillerapplication_set.count()

    def to_representation(self, instance):
        data = super(BountySerializer, self).to_representation(instance)

        # add 'user_has_applied' if the request contains a current user
        # and the bounty requries fulfillers to obtain approval
        if (
                instance.fulfillers_need_approval and
                'request' in self.context and
                self.context['request'].current_user
        ):
            user_has_applied = FulfillerApplication.objects.filter(
                bounty=instance.pk,
                applicant=self.context['request'].current_user.pk
            ).first()

            data.update({'user_has_applied': not not user_has_applied})
            data.update(
                {'user_can_fulfill': user_has_applied and user_has_applied.state == FulfillerApplication.ACCEPTED})

        return data


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
    categories = CreatableSlugRelatedField(
        many=True, slug_field='name', queryset=Category.objects.all())
    token_contract = serializers.CharField(required=False, allow_blank=True)
    token_symbol = serializers.CharField(read_only=True)
    token_decimals = serializers.IntegerField(read_only=True)
    arbiter = serializers.CharField(allow_blank=True, required=False)
    usd_price = serializers.FloatField(read_only=True)
    on_chain = serializers.BooleanField(read_only=True)
    # current_market_token_data = TokenSerializer(read_only=True, source='token')
    attached_url = serializers.CharField(required=False, allow_blank=True)
    uid = serializers.CharField(read_only=True)
    calculated_fulfillment_amount = serializers.DecimalField(
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
        print('validated data')
        print(validated_data)
        instance = super(DraftBountyWriteSerializer, self).create(validated_data)
        print('instance')
        print(instance)
        request = self.context.get('request')
        user = request.current_user
        instance.user = user
        token_data = map_token_data(
            str(instance.token_version),
            validated_data.get('token_contract'),
            validated_data.get('fulfillment_amount'))
        instance.token_symbol = token_data.get('token_symbol')
        instance.token_decimals = token_data.get('token_decimals')
        instance.token_contract = token_data.get('token_contract')
        instance.usd_price = token_data.get('usd_price')
        instance.issuer = user.public_address
        # instance.attached_url = validated_data.get('attached_url')
        instance.save()
        print('finished saving')
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        super(DraftBountyWriteSerializer, self).update(
            instance,
            validated_data
        )
        token_data = map_token_data(
            str(instance.token_version),
            validated_data.get('token_contract'),
            validated_data.get('fulfillment_amount'))
        instance.token_symbol = token_data.get('token_symbol')
        instance.token_decimals = token_data.get('token_decimals')
        instance.token_contract = token_data.get('token_contract')
        instance.usd_price = token_data.get('usd_price')
        instance.save()
        return instance


class FulfillerApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FulfillerApplication
        fields = '__all__'

    def to_representation(self, value):
        all_data = {
            'applicationId': value.id,
            'applicant': UserSerializer(value.applicant).data,
            'message': value.message,
            'created': value.created,
            'modified': value.modified,
            'state': value.state
        }

        if 'request' in self.context:
            if value.bounty.user == self.context['request'].current_user:
                return all_data

            if (value.applicant == self.context['request'].current_user and value.state == 'R') or (value.state == 'A'):
                return {
                    'applicationId': value.id,
                    'applicant': UserSerializer(value.applicant).data,
                    'state': value.state
                }

            return {
                'applicationId': value.id,
                'applicant': UserSerializer(value.applicant).data,
            }
        else:
            return all_data


class FulfillerApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FulfillerApplication
        fields = '__all__'
