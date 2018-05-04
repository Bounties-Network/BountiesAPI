from rest_framework import serializers
from notifications.models import DashboardNotification


class NotificationSerializer(serializers.Notification):
    class Meta:
        model = DashboardNotification
        fields = '__all__'


class DasbhoardNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True, source='notification')

    class Meta:
        model = DashboardNotification
        fields = '__all__'
