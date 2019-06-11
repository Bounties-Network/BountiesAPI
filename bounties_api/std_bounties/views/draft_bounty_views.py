from rest_framework.viewsets import ModelViewSet
from rest_framework_filters.backends import DjangoFilterBackend
from user.permissions import AuthenticationPermission, UserObjectPermissions
from std_bounties.models import DraftBounty
from std_bounties.serializers import DraftBountyWriteSerializer
from std_bounties.filters import DraftBountiesFilter


class DraftBountyWriteViewSet(ModelViewSet):
    queryset = DraftBounty.objects.filter(on_chain=False)
    serializer_class = DraftBountyWriteSerializer
    lookup_field = 'uid'
    filter_class = DraftBountiesFilter
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('issuer',)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        elif self.action == 'create':
            permission_classes = [AuthenticationPermission]
        else:
            permission_classes = [
                AuthenticationPermission,
                UserObjectPermissions]
        return [permission() for permission in permission_classes]
