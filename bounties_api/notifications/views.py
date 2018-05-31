from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_filters.backends import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from authentication.permissions import UserIDMatches, AuthenticationPermission, UserObjectPermissions
from notifications.models import DashboardNotification
from notifications.serializers import DashboardNotificationSerializer
from notifications.filters import DashboardNotificationFilter


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AuthenticationPermission, UserIDMatches,)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return DashboardNotification.objects.filter(notification__user=user_id).order_by('created')
    serializer_class = DashboardNotificationSerializer


class NotificationViewed(APIView):
    permission_classes = (AuthenticationPermission, UserObjectPermissions)

    def get(self, request, notification_id):
        notification = get_object_or_404(DashboardNotification, id=notification_id)
        self.check_object_permissions(request, notification.notification)
        notification.viewed = True
        notification.save()
        return HttpResponse('success')


class NotificationViewAll(APIView):
    permission_classes = (AuthenticationPermission, UserIDMatches,)

    def get(self, request, user_id):
        notifications = DashboardNotification.objects.filter(notification__user__id=user_id)
        notifications.update(viewed=True)
        return HttpResponse('success')
