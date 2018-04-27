from rest_framework import viewsets
from rest_framework.response import Response
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from bounties.utils import dictfetchall
from std_bounties.constants import STAGE_CHOICES
from std_bounties.models import Bounty, Fulfillment, RankedCategory, Token
from std_bounties.queries import LEADERBOARD_QUERY
from std_bounties.serializers import BountySerializer, FulfillmentSerializer, RankedCategorySerializer, LeaderboardSerializer, TokenSerializer
from std_bounties.filters import BountiesFilter, FulfillmentsFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend


class BountyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BountySerializer
    queryset = Bounty.objects.all().prefetch_related(
        'categories').select_related('token').distinct()
    filter_class = BountiesFilter
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = (
        'fulfillmentAmount',
        'deadline',
        'bounty_created',
        'usd_price')
    search_fields = ('title', 'description', 'categories__normalized_name', 'issuer')


class FulfillmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FulfillmentSerializer
    queryset = Fulfillment.objects.all().select_related('bounty')
    filter_class = FulfillmentsFilter
    filter_backends = (DjangoFilterBackend,)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RankedCategorySerializer
    queryset = RankedCategory.objects.all()
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('total_count',)
    ordering = ('-total_count',)
    search_fields = ('normalized_name',)


class UserProfile(APIView):
    def get(self, request, address=''):
        ordered_fulfillments = Fulfillment.objects.filter(
            fulfiller=address.lower()).order_by('-created')
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


class Leaderboard(APIView):
    def get(self, request):
        cursor = connection.cursor()
        cursor.execute(LEADERBOARD_QUERY)
        query_result = dictfetchall(cursor)
        serializer = LeaderboardSerializer(query_result, many=True)
        return JsonResponse(serializer.data, safe=False)


class BountyStats(APIView):
    def get(self, request, address=''):
        bounty_stats = {}
        user_bounties = Bounty.objects.filter(issuer=address.lower())
        for stage in STAGE_CHOICES:
            bounty_stats[stage[1]] = user_bounties.filter(
                bountyStage=stage[0]).count()
        bounties_count = user_bounties.count()
        bounties_accepted_count = user_bounties.filter(
            fulfillments__accepted=True).count()
        bounties_acceptance_rate = bounties_accepted_count / \
            bounties_count if bounties_accepted_count > 0 else 0
        user_submissions = Fulfillment.objects.filter(fulfiller=address)
        submissions_count = user_submissions.count()
        submissions_accepted_count = user_submissions.filter(
            accepted=True).count()
        submissions_acceptance_rate = submissions_accepted_count / \
            submissions_count if submissions_count > 0 else 0
        profile_stats = {
            'bounties': bounties_count,
            'bounties_accepted': bounties_accepted_count,
            'bounties_acceptance_rate': bounties_acceptance_rate,
            'submissions': submissions_count,
            'submissions_accepted_count': submissions_accepted_count,
            'submissions_acceptance_rate': submissions_acceptance_rate,
        }
        return JsonResponse({**bounty_stats, **profile_stats})


class Tokens(APIView):
    def get(self, request):
        token_qs = {}
        result = []
        token_to_append = {}
        token_count = {}
        token_count = Bounty.objects.values('tokenSymbol','tokenContract',
        'tokenDecimals').annotate(count=Count('tokenSymbol')).order_by('-count')
        for bounty in token_count:
            token_to_append = {}
            token_to_append.update(bounty)
            token_qs = Token.objects.filter(symbol=bounty['tokenSymbol'])
            if token_qs.count() > 0:
                serializer = TokenSerializer(token_qs, many=True)
                token_to_append['token'] = serializer.data
            else:
                token_to_append['token'] = []
            result.append(token_to_append)
        return JsonResponse(result, safe=False)
