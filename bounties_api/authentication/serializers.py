from rest_framework import serializers
from django.apps import apps
from bounties.serializers import CreatableSlugRelatedField
from authentication.models import User, Settings
from notifications.constants import push_notification_options


class UserSerializer(serializers.ModelSerializer):
    categories = CreatableSlugRelatedField(many=True, slug_field='name', read_only=True)


    class Meta:
        model = User
        exclude = ('nonce',)


class EmailsSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        if 'issuer' not in data or 'fulfiller' not in data:
            raise serializers.ValidationError({
                'error': 'issuer or fulfiller root field required'
            })
        issuer_validations = push_notification_options['issuer']
        issuer_fields = data.get('issuer')
        for key, value in issuer_fields.items():
            if key not in issuer_validations or type(value) != bool:
                raise serializers.ValidationError({
                    key: 'This is not a valid field for an issuer'
                })
        for key, value in issuer_validations.items():
            if key not in issuer_fields:
                raise serializers.ValidationError({
                    key: 'This field is required for an issuer'
                })

        fulfiller_validations = push_notification_options['fulfiller']
        fulfiller_fields = data.get('fulfiller')

        return data


    def to_representation(self, obj):
        return obj


class SettingsSerializer(serializers.ModelSerializer):
    emails = EmailsSerializer()

    class Meta:
        model = Settings
        fields = '__all__'
