from rest_framework import serializers
from std_bounties.models import Bounty, Fulfillment
from std_bounties.constants import STAGE_CHOICES

class BountySerializer(serializers.ModelSerializer):
	bountyStage = serializers.ChoiceField(choices=STAGE_CHOICES)

	class Meta:
		model = Bounty
		fields = '__all__'

class FulfillmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fulfillment
        fields = '__all__'
