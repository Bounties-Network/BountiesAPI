from rest_framework import serializers
from django.apps import apps
from bounties.serializers import CreatableSlugRelatedField
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    categories = CreatableSlugRelatedField(many=True, slug_field='name', queryset=apps.get_model('std_bounties', 'Category').objects.all())

    class Meta:
        model = User
        exclude = ('nonce',)
