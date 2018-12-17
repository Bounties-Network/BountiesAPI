import json
from rest_framework import serializers
from bounties.serializers import CreatableSlugRelatedField
from user.models import Language, User, Settings, Skill, RankedSkill
from notifications.constants import push_notification_options


def validate_email_settings(validations, fields, label):
    if not isinstance(fields, dict):
        raise serializers.ValidationError({
            'emails': 'both, issuer, and fulfiller fields must be dictionaries'
        })
    for key, value in fields.items():
        if key not in validations or not isinstance(value, bool):
            raise serializers.ValidationError({
                key: 'This is not a valid field for a {}'.format(label)
            })
    for key in validations:
        if key not in fields:
            raise serializers.ValidationError({
                key: 'This field is required for a {}'.format(label)
            })


class EmailsSerializer(serializers.JSONField):
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
        validate_email_settings(
            fulfiller_validations,
            fulfiller_fields,
            'fulfiller')
        both_validations = push_notification_options['both']
        both_fields = data.get('both')
        validate_email_settings(both_validations, both_fields, 'both')

        return data

    def to_representation(self, obj):
        if not isinstance(obj, dict):
            return json.loads(obj)
        else:
            return obj


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = [
            'name',
            'normalized_name'
        ]


class RankedSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankedSkill
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'name',
            'normalized_name'
        ]


class SettingsSerializer(serializers.ModelSerializer):
    emails = EmailsSerializer()

    class Meta:
        model = Settings
        exclude = ('id',)


class UserSerializer(serializers.ModelSerializer):
    languages = CreatableSlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )

    skills = CreatableSlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )

    page_preview = serializers.CharField(max_length=256, read_only=True)

    settings = SettingsSerializer()

    class Meta:
        model = User
        exclude = ('nonce', 'profile_touched_manually',)


class UserInfoSerializer(serializers.ModelSerializer):
    languages = CreatableSlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )

    skills = CreatableSlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = User
        exclude = (
            'id',
            'nonce',
            'profile_touched_manually',
            'settings',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    def validate(self, data):
        twitter = data.get('twitter')
        github = data.get('github')

        if twitter and twitter[0] == '@' or github and github[0] == '@':
            raise serializers.ValidationError("social media handles must not include @ symbol")

        return data

    class Meta:
        model = User
        fields = (
            'name',
            'email',
            'wants_marketing_emails',
            'organization',
            'small_profile_image_url',
            'large_profile_image_url',
            'website',
            'twitter',
            'github',
            'linkedin',
        )
