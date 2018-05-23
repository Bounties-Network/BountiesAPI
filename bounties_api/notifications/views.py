from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_filters.backends import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from notifications.models import DashboardNotification
from notifications.serializers import DashboardNotificationSerializer
from notifications.filters import DashboardNotificationFilter


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return DashboardNotification.objects.filter(notification__user=user_id).order_by('created')
    serializer_class = DashboardNotificationSerializer

class NotificationViewed(APIView):
    # This view needs to only be accessible if the user is logged in
    def get(self, request, notification_id):
        notification = get_object_or_404(DashboardNotification, id=notification_id)
        notification.viewed = True
        notification.save()
        return HttpResponse('success')
