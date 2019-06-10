from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from user.permissions import AuthenticationPermission
from std_bounties.models import Bounty, Fulfillment
from std_bounties.serializers import ReviewSerializer
from notifications.notification_client import NotificationClient
notification_client = NotificationClient()


class FulfillmentReviews(APIView):
    permission_classes = [AuthenticationPermission]

    @staticmethod
    def get(_, bounty_id, fulfillment_id):
        bounty = get_object_or_404(Bounty, bounty_id=bounty_id)
        fulfillment = get_object_or_404(
            Fulfillment,
            bounty=bounty,
            fulfillment_id=fulfillment_id,
            accepted=True)
        issuer_review = fulfillment.issuer_review
        fulfiller_review = fulfillment.fulfiller_review
        issuer_review_data = ReviewSerializer(
            issuer_review).data if issuer_review else None
        fulfiller_review_data = ReviewSerializer(
            fulfiller_review).data if fulfiller_review else None
        return JsonResponse({
            'issuer_review': issuer_review_data,
            'fulfiller_review': fulfiller_review_data,
        })

    @staticmethod
    def post(request, bounty_id, fulfillment_id):
        bounty = get_object_or_404(Bounty, pk=bounty_id)
        fulfillment = get_object_or_404(
            Fulfillment,
            bounty=bounty,
            fulfillment_id=fulfillment_id,
            accepted=True)
        current_user = request.current_user
        reviewer = None
        reviewee = None

        if fulfillment.user == current_user and not fulfillment.issuer_review:
            reviewer = fulfillment.user
            reviewee = bounty.user

        if bounty.user == current_user and not fulfillment.fulfiller_review:
            reviewer = bounty.user
            reviewee = fulfillment.user

        if not reviewer:
            return HttpResponse('Unauthorized', status=401)

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save(reviewer=reviewer, reviewee=reviewee)
        if fulfillment.user == current_user:
            fulfillment.issuer_review = review
        else:
            fulfillment.fulfiller_review = review
        fulfillment.save()
        notification_client.rating_issued(
            bounty_id=bounty_id,
            review=review,
            uid=fulfillment_id,
            reviewer=reviewer,
            reviewee=reviewee)
        notification_client.rating_received(
            bounty_id=bounty_id,
            review=review,
            uid=fulfillment_id,
            reviewer=reviewer,
            reviewee=reviewee)
        return JsonResponse(data=serializer.data)
