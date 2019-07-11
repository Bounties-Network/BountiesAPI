from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from std_bounties.models import Comment, Bounty, Fulfillment
from std_bounties.serializers import CommentSerializer
from user.permissions import AuthenticationPermission
from notifications.notification_client import NotificationClient
notification_client = NotificationClient()


class BountyComments(ListModelMixin, GenericViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'POST':
            permission_classes = [AuthenticationPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Comment.objects.filter(bounty__id=self.kwargs['bounty_id']).order_by('-created')

    @staticmethod
    def post(request, bounty_id):
        bounty = get_object_or_404(Bounty, pk=bounty_id)

        serializer = CommentSerializer(
            data=request.data,
            context={
                'request': request
            }
        )

        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        bounty.comments.add(comment)

        notification_client.comment_issued(bounty.pk, comment.created, comment.id)
        notification_client.comment_received(bounty.pk, comment.created, comment.id)

        return JsonResponse(serializer.data)


class FulfillmentComments(ListModelMixin, GenericViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'POST':
            permission_classes = [AuthenticationPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Comment.objects.filter(fulfillment__id=self.kwargs['fulfillment_id']).order_by('-created')

    @staticmethod
    def post(request, fulfillment_id):
        fulfillment = get_object_or_404(Fulfillment, id=fulfillment_id)

        serializer = CommentSerializer(
            data=request.data,
            context={
                'request': request
            }
        )

        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        fulfillment.comments.add(comment)

        notification_client.fulfillment_comment_issued(fulfillment.bounty_id, fulfillment_id, comment.created, comment.id)
        notification_client.fulfillment_comment_received(fulfillment.bounty_id, fulfillment_id, comment.created, comment.id)

        return JsonResponse(serializer.data)
