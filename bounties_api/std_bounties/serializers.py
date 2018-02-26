from rest_framework import serializers
from std_bounties.models import Bounty, Fulfillment

class BountySerializer(serializers.ModelSerializer):

    class Meta:
        model = Bounty
        fields = '__all__'

class FulfillmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fulfillment
        fields = '__all__'
