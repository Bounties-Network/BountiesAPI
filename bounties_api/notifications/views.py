from rest_framework import viewsets
from rest_framework.views import APIView
from notifications.models import DashboardNotification
from notifications.serializers import DashboardNotificationSerializer
from notifications.filters import DashboardNotificationFilter


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DashboardNotificationSerializer
    queryset = DashboardNotification.objects.all().select_related('notification')
    filter_class = DashboardNotificationFilter
    filter_backends = (DjangoFilterBackend,)

class NotificationViewed(APIView):
    # This view needs to only be accessible if the user is logged in
    def get(self, request, notification_id):
        notification = getOr404(DashboardNotification, id=notification_id)
        notification.viewed = True
        notification.save()
