import json
from rest_framework import serializers
from django.apps import apps
from bounties.serializers import CreatableSlugRelatedField
from authentication.models import User, Settings
from notifications.constants import push_notification_options


def validate_email_settings(validations, fields, label):
    if type(fields) != dict:
        raise serializers.ValidationError({
                'emails': 'both, issuer, and fulfiller fields must be dictionaries'
            })
    for key, value in fields.items():
        if key not in validations or type(value) != bool:
            raise serializers.ValidationError({
                    key: 'This is not a valid field for a {}'.format(label)
                })
    for key in validations:
        if key not in fields:
            raise serializersValidationError({
                    key: 'This field is required for a {}'.format(label)
                })

class EmailsSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        if 'issuer' not in data or 'fulfiller' not in data or 'both' not in data:
            raise serializers.ValidationError({
                'error': 'issuer, fulfiller, or both root field required'
            })
        issuer_validations = push_notification_options['issuer']
        issuer_fields = data.get('issuer')
        validate_email_settings(issuer_validations, issuer_fields, 'issuer')
        fulfiller_validations = push_notification_options['fulfiller']
        fulfiller_fields = data.get('fulfiller')
        validate_email_settings(fulfiller_validations, fulfiller_fields, 'fulfiller')
        both_validations = push_notification_options['both']
        both_fields = data.get('both')
        validate_email_settings(both_validations, both_fields, 'both')

        return json.dumps(data)


    def to_representation(self, obj):
        if type(obj) != dict:
            return json.loads(obj)
        else:
            return obj


class SettingsSerializer(serializers.ModelSerializer):
    emails = EmailsSerializer()

    class Meta:
        model = Settings
        exclude = ('id',)


class UserSerializer(serializers.ModelSerializer):
    categories = CreatableSlugRelatedField(many=True, slug_field='name', read_only=True)
    settings = SettingsSerializer()

    class Meta:
        model = User
        exclude = ('nonce', 'profile_hash',)
