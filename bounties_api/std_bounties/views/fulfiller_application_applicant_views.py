from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from user.permissions import AuthenticationPermission, ApplicantPermissions
from std_bounties.models import FulfillerApplication
from std_bounties.serializers import FulfillerApplicantSerializer
from notifications.notification_client import NotificationClient
notification_client = NotificationClient()


class FulfillerApplicationApplicantView(GenericAPIView, UpdateModelMixin):
    queryset = FulfillerApplication.objects.all()
    serializer_class = FulfillerApplicantSerializer

    def get_permissions(self):
        permission_classes = []

        if self.request.method == 'PUT':
            permission_classes = [
                AuthenticationPermission,
                ApplicantPermissions
            ]

        return [permission() for permission in permission_classes]

    def put(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        application = get_object_or_404(FulfillerApplication, pk=response.data['id'])

        if application.state == FulfillerApplication.ACCEPTED:
            notification_client.application_accepted_applicant(application.bounty, application)
            notification_client.application_accepted_issuer(application.bounty, application)

        elif application.state == FulfillerApplication.REJECTED:
            notification_client.application_rejected_applicant(application.bounty, application)
            notification_client.application_rejected_issuer(application.bounty, application)

        return response
