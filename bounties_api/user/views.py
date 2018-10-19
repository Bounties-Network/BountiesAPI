from rest_framework.views import APIView
from rest_framework import viewsets
from datetime import datetime
from user.backend import authenticate, login, logout, setLastViewed, loginJWT
from user.serializers import LanguageSerializer, UserSerializer, UserInfoSerializer, UserProfileSerializer, SettingsSerializer, RankedSkillSerializer
from user.models import Language, User, RankedSkill
from user.permissions import AuthenticationPermission, UserIDMatches
from std_bounties.models import Fulfillment
from django.conf import settings
from django.db.models import Sum, Avg, Count
from django.http import JsonResponse, HttpResponse
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend
from notifications.notification_client import NotificationClient
from std_bounties.seo_client import SEOClient
from uuid import uuid4
import boto3

notification_client = NotificationClient()
seo_client = SEOClient()


class Login(APIView):
    def post(self, request):
        '''
        Logs in the user

        Expects `public_address` and `signature` in `data` on the request

        Returns the serialized user
        '''
        public_address = request.data.get('public_address', '')
        signature = request.data.get('signature', '')
        user = authenticate(public_address=public_address, signature=signature)
        if not user:
            return HttpResponse('Unauthorized', status=401)
        login(request, user)
        return JsonResponse(UserSerializer(user).data)


class LoginJWT(APIView):
    def post(self, request):
        public_address = request.data.get('public_address', '')
        signature = request.data.get('signature', '')
        user = authenticate(public_address=public_address, signature=signature)
        if not user:
            return HttpResponse('Unauthorized', status=401)
        jwt_token = loginJWT(request, user)
        return JsonResponse({
            'user': UserSerializer(user).data,
            'token': jwt_token.decode('utf-8')
        })


class Logout(APIView):
    def get(self, request):
        '''
        Logs out the user that is currently logged in
        '''
        logout(request)
        return HttpResponse('Success')


class Nonce(APIView):
    def get(self, request, public_address=''):
        '''
        Returns nonce and user information

        Expects a public_address

        Returns:
        {
            'nonce': user.nonce,
            'has_signed_up': bool(user.email) and bool(user.name)
        }
        '''
        user = User.objects.get_or_create(
            public_address=public_address.lower())[0]
        return JsonResponse(
            {'nonce': user.nonce, 'has_signed_up': bool(user.email) and bool(user.name)})


class DismissSignup(APIView):
    permission_classes = [AuthenticationPermission, UserIDMatches]

    def get(self, request, public_address=''):
        user = User.objects.get(public_address=public_address.lower())
        user.dismissed_signup_prompt = datetime.utcnow()
        user.save()
        return JsonResponse(UserSerializer(request.current_user).data)


class UserView(APIView):
    def get(self, request):
        '''
        Returns the currently logged in user

        Expects `current_user` on the request
        '''
        if request.is_logged_in:
            setLastViewed(request, request.current_user)
            return JsonResponse(UserSerializer(request.current_user).data)
        return HttpResponse('Unauthorized', status=401)


class RequestProfileImageUploadURL(APIView):
    permission_classes = [AuthenticationPermission]

    def get(self, request):
        '''
        Returns small and large upload URLs

        Expects `current_user` on the request

        Returns:
        {
            'sm_url': 'https://{}/{}'.format(bucket, sm_key),
            'sm_put_url': sm_put_url,
            'lg_url': 'https://{}/{}'.format(bucket, lg_key),
            'lg_put_url': lg_put_url
        }
        '''
        AWS_REGION = 'us-east-1'
        client = boto3.client('s3', region_name=AWS_REGION)

        current_user = request.current_user
        nonce = str(uuid4())[:4]
        bucket = 'assets.bounties.network'

        sm_key = '{}/userimages/{}-sm-{}.png'.format(
            settings.ENVIRONMENT, current_user.public_address, nonce)
        lg_key = '{}/userimages/{}-lg-{}.png'.format(
            settings.ENVIRONMENT, current_user.public_address, nonce)

        sm_put_url = client.generate_presigned_url(
            'put_object',
            Params={
                'ContentType': 'image/png',
                'Bucket': bucket,
                'ACL': 'public-read',
                'Key': sm_key}
        )

        lg_put_url = client.generate_presigned_url(
            'put_object',
            Params={
                'ContentType': 'image/png',
                'Bucket': bucket,
                'ACL': 'public-read',
                'Key': lg_key}
        )

        return JsonResponse({
            'sm_url': 'https://{}/{}'.format(bucket, sm_key),
            'sm_put_url': sm_put_url,
            'lg_url': 'https://{}/{}'.format(bucket, lg_key),
            'lg_put_url': lg_put_url
        })


class SettingsView(APIView):
    def post(self, request):
        '''
        Saves the data as settings, then saves the user

        Expects `current_user` and `data` on the request

        Returns the serialized settings
        '''
        serializer = SettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        settings = serializer.save()
        user = request.current_user
        user.settings = settings
        user.save()
        return JsonResponse(SettingsSerializer(settings).data)

    def put(self, request):
        '''
        Saves the data through the serializer

        Expects `current_user` and `data` on the request

        Returns the updated serialized settings
        '''
        user = request.current_user
        settings = user.settings
        serializer = SettingsSerializer(settings, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_settings = serializer.save()
        return JsonResponse(SettingsSerializer(updated_settings).data)


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Returns ordered languages
    '''
    serializer_class = LanguageSerializer
    queryset = Language.objects.order_by('name')


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Returns ordered skills
    '''
    serializer_class = RankedSkillSerializer
    queryset = RankedSkill.objects.all()
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('total_count',)
    ordering = ('-total_count',)
    search_fields = ('normalized_name',)


class UserInfo(APIView):
    def get(self, request, public_address):
        '''
        Returns the serialized user info

        Expects `public_address`
        '''
        try:
            user = User.objects.get(public_address=public_address.lower())
        except User.DoesNotExist:
            return HttpResponse('Not Found', status=404)

        serializer = UserInfoSerializer(user)
        return JsonResponse(serializer.data)


class UserProfile(APIView):
    def post(self, request, public_address):
        '''
        Saves the user profile using `data`

        Expects `public_address` and `current_user` and `data` on the request

        Returns the serialized user
        '''
        user = request.current_user

        user.profile_touched_manually = True

        serializer = UserProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user.save_and_clear_skills(request.data.get('skills'))
        user.save_and_clear_languages(request.data.get('languages'))

        user.save()

        notification_client.profile_updated(user.public_address.lower())
        seo_client.profile_preview_screenshot(user.id)

        return JsonResponse(UserProfileSerializer(user).data)

    def get(self, request, public_address):
        '''
        Returns JSON response with user information

        Expects `public_address`

        Returns:
        {
            'user': serializer.data,
            'stats': profile_stats
        }
        '''
        try:
            user = User.objects.get(public_address=public_address.lower())
        except User.DoesNotExist:
            return JsonResponse({'user': None, 'stats': {}})

        platform = request.GET.get('platform__in', None)
        additional_filters = {}

        if platform:
            additional_filters.update({'platform__in': platform.split(',')})

        user_bounties = user.bounty_set.filter(**additional_filters)
        user_fulfillments = user.fulfillment_set.filter(**additional_filters)
        user_reviews = user.reviews.filter(**additional_filters)
        user_reviewees = user.reviewees.filter(**additional_filters)

        awarded = Fulfillment.objects.filter(
            accepted=True, bounty__user=user, **additional_filters).aggregate(
            Sum('usd_price'))
        earned = user_fulfillments.filter(
            accepted=True).aggregate(
            Sum('usd_price'))
        issuer_ratings_given = user_reviews.filter(
            fulfillment_review__isnull=False).aggregate(
            Avg('rating'))
        issuer_ratings_received = user_reviewees.filter(
            issuer_review__isnull=False).aggregate(Avg('rating'))
        fulfiller_ratings_given = user_reviews.filter(
            issuer_review__isnull=False).aggregate(
            Avg('rating'))
        fulfiller_ratings_received = user_reviewees.filter(
            fulfillment_review__isnull=False).aggregate(Avg('rating'))
        issuer_fulfillment_acceptance = None if not Fulfillment.objects.filter(
            bounty__user=user, **additional_filters).count() else (
            Fulfillment.objects.filter(
                accepted=True,
                bounty__user=user, **additional_filters).count() /
            Fulfillment.objects.filter(
                bounty__user=user, **additional_filters).count())
        fulfiller_fulfillment_acceptance = None if not user_fulfillments.count() else (
            user_fulfillments.filter(accepted=True).count() / user_fulfillments.count())

        total_fulfillments_on_bounties = user_bounties.annotate(
            fulfillments_count=Count('fulfillments')).aggregate(
            Sum('fulfillments_count')
        ).get('fulfillments_count__sum', None)

        if not total_fulfillments_on_bounties:
            total_fulfillments_on_bounties = 0

        profile_stats = {
            'awarded': awarded.get('usd_price__sum'),
            'earned': earned.get('usd_price__sum'),
            'issuer_ratings_given': issuer_ratings_given.get('rating__avg'),
            'issuer_ratings_received': issuer_ratings_received.get('rating__avg'),
            'fulfiller_ratings_given': fulfiller_ratings_given.get('rating__avg'),
            'fulfiller_ratings_received': fulfiller_ratings_received.get('rating__avg'),
            'issuer_fulfillment_acceptance': issuer_fulfillment_acceptance,
            'fulfiller_fulfillment_acceptance': fulfiller_fulfillment_acceptance,
            'total_bounties': user_bounties.count(),
            'total_fulfillments': user_fulfillments.count(),
            'total_fulfillments_on_bounties': total_fulfillments_on_bounties
        }
        serializer = UserSerializer(user)

        return JsonResponse({'user': serializer.data, 'stats': profile_stats})
