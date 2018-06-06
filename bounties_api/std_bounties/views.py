from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from bounties.utils import dictfetchall, extractInParams, sqlGenerateOrList, limitOffsetParams
from std_bounties.constants import STAGE_CHOICES
from std_bounties.queries import LEADERBOARD_ISSUER_QUERY, LEADERBOARD_FULFILLER_QUERY
from std_bounties.serializers import BountySerializer, FulfillmentSerializer, RankedCategorySerializer, LeaderboardIssuerSerializer, LeaderboardFulfillerSerializer, TokenSerializer, DraftBountyWriteSerializer, CommentSerializer, ReviewSerializer
from std_bounties.models import Bounty, DraftBounty, Fulfillment, RankedCategory, Token, Comment
from std_bounties.filters import BountiesFilter, FulfillmentsFilter, RankedCategoryFilter
from authentication.permissions import AuthenticationPermission, UserObjectPermissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend


class SubmissionReviews(APIView):
    permission_classes = [AuthenticationPermission]

    def post(self, request, bounty_id, fulfillment_id):
        bounty = get_object_or_404(Bounty, bounty_id=bounty_id)
        fulfillment = get_object_or_404(Fulfillment, bounty=bounty, fulfillment_id=fulfillment_id, accepted=True)
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

        serializer = ReviewSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save(reviewer=reviewer, reviewee=reviewee)
        return JsonResponse(data=serializer.data)



class BountyComments(APIView):
    permission_classes = [AuthenticationPermission]

    def get(self, request, bounty_id):
        get_object_or_404(Bounty, bounty_id=bounty_id)
        comments = Comment.objects.filter(bounty__id=bounty_id)
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)


    def post(self, request, bounty_id):
        bounty = get_object_or_404(Bounty, bounty_id=bounty_id)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        bounty.comments.add(comment)
        return JsonResponse(serializer.data)


class DraftBountyWriteViewSet(viewsets.ModelViewSet):
    queryset = DraftBounty.objects.filter(on_chain=False)
    serializer_class = DraftBountyWriteSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user_id',)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        elif self.action == 'create':
            permission_classes = [AuthenticationPermission]
        else:
            permission_classes = [AuthenticationPermission, UserObjectPermissions]
        return [permission() for permission in permission_classes]


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
    filter_class = RankedCategoryFilter
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('total_count',)
    ordering = ('-total_count',)
    search_fields = ('normalized_name',)


class UserProfile(APIView):
    def get(self, request, address=''):
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



class LeaderboardIssuer(APIView):
    def get(self, request):
        sql_param = ''
        platform_in = extractInParams(request, 'platform', 'platform__in')
        startIndex, endIndex = limitOffsetParams(request)
        if platform_in:
            sql_param = 'AND ( '
            sql_param += sqlGenerateOrList('fulfillment.\"platform\"', len(platform_in), '=')
            sql_param += ' OR '
            sql_param += sqlGenerateOrList('bounty.\"platform\"', len(platform_in), '=')
            sql_param += ' )'
        platform_in = platform_in + platform_in

        formatted_query = LEADERBOARD_ISSUER_QUERY.format(sql_param)
        cursor = connection.cursor()
        cursor.execute(formatted_query, platform_in)
        query_result = dictfetchall(cursor)
        narrowed_result = query_result[startIndex : endIndex]
        serializer = LeaderboardIssuerSerializer(narrowed_result, many=True)
        return JsonResponse(serializer.data, safe=False)


class LeaderboardFulfiller(APIView):
    def get(self, request):
        sql_param = ''
        platform_in = extractInParams(request, 'platform', 'platform__in')
        startIndex, endIndex = limitOffsetParams(request)
        if platform_in:
            sql_param = 'AND ( '
            sql_param += sqlGenerateOrList('fulfillment.\"platform\"', len(platform_in), '=')
            sql_param += ' OR '
            sql_param += sqlGenerateOrList('bounty.\"platform\"', len(platform_in), '=')
            sql_param += ' )'
        platform_in = platform_in + platform_in

        formatted_query = LEADERBOARD_FULFILLER_QUERY.format(sql_param)
        cursor = connection.cursor()
        cursor.execute(formatted_query, platform_in)
        query_result = dictfetchall(cursor)
        narrowed_result = query_result[startIndex : endIndex]
        serializer = LeaderboardFulfillerSerializer(narrowed_result, many=True)
        return JsonResponse(serializer.data, safe=False)


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
