from rest_framework.views import APIView
from django.http import Http404, JsonResponse
from bounties.utils import extractInParams
from std_bounties.models import Fulfillment


class UserProfile(APIView):
    @staticmethod
    def get(request, address=''):
        platform_in = extractInParams(request, 'platform', 'platform__in')
        extra_filters = {}
        if platform_in:
            extra_filters['platform__in'] = platform_in
        ordered_fulfillments = Fulfillment.objects.filter(
            fulfiller=address.lower(), **extra_filters).order_by('-created')
        if not ordered_fulfillments.exists():
            raise Http404("Address does not exist")

        latest_fulfillment = ordered_fulfillments[0]
        user_profile = {
            "address": address,
            "name": latest_fulfillment.fulfiller_name,
            "email": latest_fulfillment.fulfiller_email,
            "githubUsername": latest_fulfillment.fulfiller_githubUsername,
        }
        return JsonResponse(user_profile)
