from rest_framework import serializers
from notifications.models import DashboardNotification, Transaction


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DashboardNotification
        fields = '__all__'


class DashboardNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = DashboardNotification
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    failed = serializers.BooleanField(read_only=True)
    completed = serializers.BooleanField(read_only=True)
    viewed = serializers.BooleanField(read_only=True)
    data = serializers.JSONField(read_only=True)

    class Meta:
        model = Transaction
        exclude = ('user',)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.current_user
        updated_data = {
            **validated_data,
            'user': user,
        }
        return Transaction.objects.create(**updated_data)
