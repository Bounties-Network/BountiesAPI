from rest_framework import serializers
from notifications.models import DashboardNotification, Transaction


class DashboardNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DashboardNotification
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.current_user
        updated_data = {
            **validated_data,
            'user': user,
        }
        return Transaction.objects.create(**updated_data)
