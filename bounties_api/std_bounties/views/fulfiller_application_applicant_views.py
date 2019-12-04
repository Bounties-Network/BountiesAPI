from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from user.permissions import AuthenticationPermission, ApplicantPermissions
from std_bounties.models import FulfillerApplication, Bounty, Activity
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
        bounty = Bounty.objects.get(id=application.bounty_id)
        if application.state == FulfillerApplication.ACCEPTED:
            Activity.objects.get_or_create(
                bounty_id=application.bounty_id,
                event_type='ApplicationAccepted',
                user_id=bounty.user_id,
                defaults={
                    'event_type': 'ApplicationAccepted',
                    'bounty_id': application.bounty_id,
                    'user_id': bounty.user_id,
                    'community_id': bounty.community_id,
                    'date': application.modified
                }
            )
            notification_client.application_accepted_applicant(application.bounty, application)
            notification_client.application_accepted_issuer(application.bounty, application)

        elif application.state == FulfillerApplication.REJECTED:
            Activity.objects.get_or_create(
                bounty_id=application.bounty_id,
                event_type='ApplicationRejected',
                user_id=bounty.user_id,
                defaults={
                    'event_type': 'ApplicationRejected',
                    'bounty_id': application.bounty_id,
                    'user_id': bounty.user_id,
                    'community_id': bounty.community_id,
                    'date': application.modified
                }
            )
            notification_client.application_rejected_applicant(application.bounty, application)
            notification_client.application_rejected_issuer(application.bounty, application)

        return response
