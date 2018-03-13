from rest_framework import viewsets
from rest_framework.response import Response
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from std_bounties.constants import STAGE_CHOICES
from std_bounties.models import Bounty, Fulfillment, RankedCategory
from std_bounties.serializers import BountySerializer, FulfillmentSerializer, RankedCategorySerializer
from std_bounties.filters import BountiesFilter, FulfillmentsFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend


class BountyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = BountySerializer
    queryset = Bounty.objects.all()
    filter_class = BountiesFilter
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('fulfillmentAmount', 'deadline', 'bounty_created', 'usd_price')
    search_fields = ('title', 'description', 'categories__normalized_name')


class FulfillmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = FulfillmentSerializer
    queryset = Fulfillment.objects.all()
    filter_class = FulfillmentsFilter
    filter_backends = (DjangoFilterBackend,)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = RankedCategorySerializer
    queryset = RankedCategory.objects.all()
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('total_count',)
    ordering = ('-total_count',)
    search_fields = ('normalized_name',)


class UserProfile(APIView):
    def get(self, request, address=''):
        ordered_fulfillments = Fulfillment.objects.filter(fulfiller=address).order_by('-created')
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


class BountyStats(APIView):
    def get(self, request, address=''):
        bounty_stats = {}
        user_bounties = Bounty.objects.filter(issuer=address)
        for stage in STAGE_CHOICES:
            bounty_stats[stage[1]] = user_bounties.filter(bountyStage=stage[0]).count()
        return JsonResponse(bounty_stats)


class ProfileStats(APIView):
    def get(self, request, address=''):
        user_bounties = Bounty.objects.filter(issuer=address)
        bounties_count = user_bounties.count()
        bounties_accepted_count = user_bounties.filter(fulfillments__accepted=True).count()
        bounties_acceptance_rate = bounties_accepted_count/bounties_count if bounties_accepted_count > 0 else 0
        user_submissions = Fulfillment.objects.filter(fulfiller=address)
        submissions_count = user_submissions.count()
        submissions_accepted_count = user_submissions.filter(accepted=True).count()
        submissions_acceptance_rate = submissions_accepted_count/submissions_count if submissions_count > 0 else 0
        profile_stats = {
            'bounties': bounties_count,
            'bounties_accepted': bounties_accepted_count,
            'bounties_acceptance_rate': bounties_acceptance_rate,
            'submissions': submissions_count,
            'submissions_accepted_count': submissions_accepted_count,
            'submissions_acceptance_rate': submissions_acceptance_rate,
        }
        return JsonResponse(profile_stats)
