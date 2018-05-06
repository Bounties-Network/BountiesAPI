import rest_framework_filters as filters


class NotificationFilter(filters.FilterSet):
    class Meta:
        model = 
        fields = {
            'user_id': ['notification__user']
        }
