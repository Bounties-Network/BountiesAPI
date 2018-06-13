from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_filters.backends import DjangoFilterBackend
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from authentication.permissions import UserIDMatches, AuthenticationPermission, UserObjectPermissions
from notifications.models import DashboardNotification, Transaction
from notifications.serializers import DashboardNotificationSerializer, TransactionSerializer
from notifications.filters import DashboardNotificationFilter


class TransactionViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AuthenticationPermission, UserIDMatches]
        return [permission() for permission in permission_classes]


    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Transaction.objects.filter(user_id=user_id).order_by('-created')
    serializer_class = TransactionSerializer


class NotificationActivityViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return DashboardNotification.objects.filter(notification__user=user_id, is_activity=True).order_by('-created')
    serializer_class = DashboardNotificationSerializer


class NotificationPushViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return DashboardNotification.objects.filter(notification__user=user_id, is_activity=False).order_by('-created')
    serializer_class = DashboardNotificationSerializer


class NotificationViewed(APIView):
    permission_classes = (AuthenticationPermission, UserObjectPermissions)

    def get(self, request, notification_id):
        notification = get_object_or_404(DashboardNotification, id=notification_id)
        self.check_object_permissions(request, notification.notification)
        notification.viewed = True
        notification.save()
        return HttpResponse('success')


class NotificationActivityViewAll(APIView):
    permission_classes = (AuthenticationPermission, UserIDMatches,)

    def get(self, request, user_id):
        notifications = DashboardNotification.objects.filter(notification__user__id=user_id, is_activity=True)
        notifications.update(viewed=True)
        return HttpResponse('success')


class NotificationPushViewAll(APIView):
    permission_classes = (AuthenticationPermission, UserIDMatches,)

    def get(self, request, user_id):
        notifications = DashboardNotification.objects.filter(notification__user__id=user_id, is_activity=False)
        notifications.update(viewed=True)
        return HttpResponse('success')
