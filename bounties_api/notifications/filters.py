import rest_framework_filters as filters
from notifications.models import DashboardNotification


class DashboardNotificationFilter(filters.FilterSet):

    class Meta:
        model = DashboardNotification
        fields = {
        }
