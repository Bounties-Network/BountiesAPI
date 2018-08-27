import rest_framework_filters as filters
from notifications.models import DashboardNotification, Transaction


class DashboardNotificationFilter(filters.FilterSet):

    class Meta:
        model = DashboardNotification
        fields = {
            'notification__platform': ['in', 'exact']
        }


class TransactionFilter(filters.FilterSet):

    class Meta:
        model = Transaction
        fields = {
            'platform': ['exact']
        }
