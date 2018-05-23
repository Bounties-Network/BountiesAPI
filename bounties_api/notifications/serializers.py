from rest_framework import serializers
from notifications.models import DashboardNotification


class DashboardNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DashboardNotification
        fields = '__all__'
