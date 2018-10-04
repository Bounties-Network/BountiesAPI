from rest_framework import viewsets
from rest_framework import mixins
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from bounties.utils import dictfetchall, extractInParams, sqlGenerateOrList, limitOffsetParams
from std_bounties.queries import LEADERBOARD_ISSUER_QUERY, LEADERBOARD_FULFILLER_QUERY
from std_bounties.serializers import BountySerializer, FulfillmentSerializer, RankedTagSerializer, LeaderboardIssuerSerializer, LeaderboardFulfillerSerializer, TokenSerializer, DraftBountyWriteSerializer, CommentSerializer, ReviewSerializer
from std_bounties.models import Bounty, DraftBounty, Fulfillment, RankedTag, Token, Comment, Review
from std_bounties.filters import BountiesFilter, DraftBountiesFilter, FulfillmentsFilter, RankedTagFilter, ReviewsFilter
from user.permissions import AuthenticationPermission, UserObjectPermissions
from notifications.notification_client import NotificationClient
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend


notification_client = NotificationClient()


class ReviewsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        review_type = self.request.GET.get('review_type', '')

        if review_type == 'fulfiller':
            return Review.objects.filter(fulfillment_review__isnull=False)
        if review_type == 'issuer':
            return Review.objects.filter(issuer_review__isnull=False)
        return Review.objects.all()

    filter_class = ReviewsFilter
    filter_backends = (DjangoFilterBackend,)


class SubmissionReviews(APIView):
    permission_classes = [AuthenticationPermission]

    def get(self, request, bounty_id, fulfillment_id):
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

    def post(self, request, bounty_id, fulfillment_id):
        bounty = get_object_or_404(Bounty, bounty_id=bounty_id)
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


class BountyComments(mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = CommentSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'POST':
            permission_classes = [AuthenticationPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Comment.objects.filter(bounty__id=self.kwargs['bounty_id']).order_by('-created')

    def post(self, request, bounty_id):
        bounty = get_object_or_404(Bounty, bounty_id=bounty_id)
        serializer = CommentSerializer(
            data=request.data,
            context={
                'request': request
            })
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        bounty.comments.add(comment)
        notification_client.comment_issued(
            bounty.bounty_id, comment.created, comment.id)
        notification_client.comment_received(
            bounty.bounty_id, comment.created, comment.id)
        return JsonResponse(serializer.data)


class DraftBountyWriteViewSet(viewsets.ModelViewSet):
    queryset = DraftBounty.objects.filter(on_chain=False)
    serializer_class = DraftBountyWriteSerializer
    lookup_field = 'uid'
    filter_class = DraftBountiesFilter
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('issuer',)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        elif self.action == 'create':
            permission_classes = [AuthenticationPermission]
        else:
            permission_classes = [
                AuthenticationPermission,
                UserObjectPermissions]
        return [permission() for permission in permission_classes]


class BountyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BountySerializer
    queryset = Bounty.objects.all().prefetch_related(
        'tags').select_related('token').distinct()
    filter_class = BountiesFilter
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = (
        'fulfillmentAmount',
        'deadline',
        'bounty_created',
        'usd_price')
    search_fields = (
        'title',
        'description',
        'tags__normalized_name',
        'issuer')


class FulfillmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FulfillmentSerializer
    queryset = Fulfillment.objects.all().select_related('bounty')

    def get_queryset(self):
        qs = Fulfillment.objects.all().select_related('bounty')

        current_user = self.request.current_user

        if current_user:
            return qs.filter(
                Q(fulfiller=current_user.public_address) |
                Q(bounty__issuer=current_user.public_address) |
                Q(bounty__private_fulfillments=False)
            )
        else:
            return Fulfillment.objects.filter(bounty__private_fulfillments=False)

        return Fulfillment.objects.none()

    filter_class = FulfillmentsFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    ordering_fields = (
        'fulfillment_created',
        'usd_price'
    )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RankedTagSerializer
    queryset = RankedTag.objects.all()
    filter_class = RankedTagFilter
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
            sql_param += sqlGenerateOrList(
                'fulfillment.\"platform\"', len(platform_in), '=')
            sql_param += ' OR '
            sql_param += sqlGenerateOrList('bounty.\"platform\"',
                                           len(platform_in), '=')
            sql_param += ' )'
        platform_in = platform_in + platform_in

        formatted_query = LEADERBOARD_ISSUER_QUERY.format(sql_param)
        cursor = connection.cursor()
        cursor.execute(formatted_query, platform_in)
        query_result = dictfetchall(cursor)
        narrowed_result = query_result[startIndex: endIndex]
        serializer = LeaderboardIssuerSerializer(narrowed_result, many=True)
        return JsonResponse({'count': len(query_result), 'results': serializer.data}, safe=False)


class LeaderboardFulfiller(APIView):
    def get(self, request):
        sql_param = ''
        platform_in = extractInParams(request, 'platform', 'platform__in')
        startIndex, endIndex = limitOffsetParams(request)
        if platform_in:
            sql_param = 'AND ( '
            sql_param += sqlGenerateOrList(
                'fulfillment.\"platform\"', len(platform_in), '=')
            sql_param += ' OR '
            sql_param += sqlGenerateOrList('bounty.\"platform\"',
                                           len(platform_in), '=')
            sql_param += ' )'
        platform_in = platform_in + platform_in

        formatted_query = LEADERBOARD_FULFILLER_QUERY.format(sql_param)
        cursor = connection.cursor()
        cursor.execute(formatted_query, platform_in)
        query_result = dictfetchall(cursor)
        narrowed_result = query_result[startIndex: endIndex]
        serializer = LeaderboardFulfillerSerializer(narrowed_result, many=True)
        return JsonResponse({'count': len(query_result), 'results': serializer.data}, safe=False)


class Tokens(APIView):
    def get(self, request):
        token_qs = {}
        result = []
        token_to_append = {}
        token_count = {}
        token_count = Bounty.objects.values(
            'tokenSymbol', 'tokenContract', 'tokenDecimals').annotate(
            count=Count('tokenSymbol')).order_by('-count')
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
