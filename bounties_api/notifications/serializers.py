from rest_framework import serializers
from notifications.models import DashboardNotification


class NotificationSerializer(serializers.Notification):
    class Meta:
        model = DashboardNotification
        fields = '__all__'


class DasbhoardNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DashboardNotification
        fields = '__all__'
