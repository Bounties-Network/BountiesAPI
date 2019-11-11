from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from user.permissions import AuthenticationPermission
from std_bounties.models import Bounty, View
from std_bounties.serializers import ViewSerializer
from notifications.notification_client import NotificationClient
notification_client = NotificationClient()


class BountyViews(APIView):
    @staticmethod
    def post(request, bounty_id):
        print('viewing bounty')
        print(bounty_id)
        bounty = get_object_or_404(Bounty, id=bounty_id)
        current_user = request.current_user

        serializer = ViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user, bounty=bounty)

        bounty.view_count += 1
        bounty.save()

        return JsonResponse(data=serializer.data)
