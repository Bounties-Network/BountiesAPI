from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from user.permissions import AuthenticationPermission
from std_bounties.models import FulfillerApplication, Bounty
from std_bounties.serializers import FulfillerApplicationSerializer
from notifications.notification_client import NotificationClient
notification_client = NotificationClient()


class FulfillerApplicationViewSet(ListModelMixin, GenericViewSet):
    serializer_class = FulfillerApplicationSerializer

    def get_permissions(self):
        permission_classes = []

        # TODO ensure bounty owner cannot create application
        # and that only bounty owner can retrieve applications
        # and that bounty is of correct type for applications

        if self.request.method == 'POST':
            permission_classes = [AuthenticationPermission]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return FulfillerApplication.objects.filter(bounty_id=self.kwargs['bounty_id']).order_by('-created')

    def post(self, request, bounty_id):
        bounty = get_object_or_404(Bounty, pk=bounty_id)

        serializer = FulfillerApplicationSerializer(
            data={
                **request.data,
                'applicant': request.current_user.pk,
                'bounty': bounty.pk
            }
        )

        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        Activity.objects.get_or_create(
            bounty_id=application.bounty_id,
            event_type='ApplicationCreated',
            user_id=application.applicant_id,
            defaults={
                'event_type': 'ApplicationCreated',
                'bounty_id': application.bounty_id,
                'user_id': application.applicant_id,
                'community_id': bounty.community_id,
                'date': application.created
            }
        )

        notification_client.application_created(bounty, application)
        notification_client.application_received(bounty, application)

        return JsonResponse(serializer.data)
