from rest_framework import serializers
from activity.models import Activity
from std_bounties.serializers import BountySerializer, CommentSerializer, FulfillmentSerializer, UserSerializer


class TargetSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if value.bounty:
            serializer = BountySerializer(value.bounty)
            return {
                'type': 'bounty',
                'data': serializer.data
            }
        elif value.draft:
            serializer = BountySerializer(value.draft)
            return {
                'type': 'draft',
                'data': serializer.data
            }
        elif value.user:
            serializer = UserSerializer(value.user)
            return {
                'type': 'user',
                'data': serializer.data
            }

        raise Exception('Unexpected type of target')


class ObjectSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if value.bounty:
            serializer = BountySerializer(value.bounty)
            return {
                'type': 'bounty',
                'data': serializer.data
            }
        elif value.draft:
            serializer = BountySerializer(value.draft)
            return {
                'type': 'draft',
                'data': serializer.data
            }
        elif value.comment:
            serializer = CommentSerializer(value.comment)
            return {
                'type': 'comment',
                'data': serializer.data
            }
        elif value.fulfillment:
            serializer = FulfillmentSerializer(value.fulfillment)
            return {
                'type': 'fulfillment',
                'data': serializer.data
            }

        raise Exception('Unexpected type of object')


class ActivitySerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)  # TODO make better user serializer
    target = TargetSerializer(read_only=True)
    object = ObjectSerializer(read_only=True)
    verb = serializers.CharField(source='get_verb_display')

    class Meta:
        model = Activity
        fields = [
            'actor',
            'verb',
            'date',
            'target',
            'object',
        ]
