from rest_framework import viewsets
from activity.models import Activity
from activity.serializers import ActivitySerializer


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return Activity.objects.all()
