import rest_framework_filters as filters


class NotificationFilter(filters.FilterSet):
    class Meta:
        model = 
        fields = {
            'notification__user': ['exact']
        }
