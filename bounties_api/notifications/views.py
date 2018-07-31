from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from user.permissions import UserIDMatches, AuthenticationPermission, UserObjectPermissions
from notifications.models import DashboardNotification, Transaction
from notifications.serializers import DashboardNotificationSerializer, TransactionSerializer


class TransactionViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AuthenticationPermission, UserIDMatches]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        public_address = self.kwargs.get('public_address', '').lower()
        return Transaction.objects.filter(
            viewed=False,
            user__public_address=public_address).order_by(
            'viewed', '-created')
    serializer_class = TransactionSerializer


class NotificationActivityViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        public_address = self.kwargs.get('public_address')
        return DashboardNotification.objects.filter(
            notification__user__public_address=public_address,
            is_activity=True).order_by('-created')
    serializer_class = DashboardNotificationSerializer


class NotificationPushViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        public_address = self.kwargs.get('public_address')
        return DashboardNotification.objects.filter(
            notification__user__public_address=public_address,
            is_activity=False).order_by('-created')
    serializer_class = DashboardNotificationSerializer


class NotificationViewed(APIView):
    permission_classes = (AuthenticationPermission, UserObjectPermissions)

    def get(self, request, notification_id):
        notification = get_object_or_404(
            DashboardNotification, id=notification_id)
        self.check_object_permissions(request, notification.notification)
        notification.viewed = True
        notification.save()
        return HttpResponse('success')


class TransactionViewed(APIView):
    permission_classes = (AuthenticationPermission, UserObjectPermissions)

    def get(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        self.check_object_permissions(request, transaction)
        transaction.viewed = True
        transaction.save()
        return HttpResponse('success')


class NotificationActivityViewAll(APIView):
    permission_classes = (AuthenticationPermission, UserIDMatches,)

    def get(self, request, public_address):
        notifications = DashboardNotification.objects.filter(
            notification__user__public_address=public_address, is_activity=True)
        notifications.update(viewed=True)
        return HttpResponse('success')


class NotificationPushViewAll(APIView):
    permission_classes = (AuthenticationPermission, UserIDMatches,)

    def get(self, request, public_address):
        notifications = DashboardNotification.objects.filter(
            notification__user__public_address=public_address, is_activity=False)
        notifications.update(viewed=True)
        return HttpResponse('success')
