from rest_framework.views import APIView
from rest_framework import viewsets
from user.backend import authenticate, login, logout
from user.serializers import LanguageSerializer, UserSerializer, UserInfoSerializer, UserProfileSerializer, SettingsSerializer, RankedSkillSerializer
from user.models import Language, User, RankedSkill
from std_bounties.models import Fulfillment
from django.db.models import Sum, Avg, Count
from django.http import JsonResponse, HttpResponse
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_filters.backends import DjangoFilterBackend
from notifications.notification_client import NotificationClient

notification_client = NotificationClient()


class Login(APIView):
    def post(self, request):
        public_address = request.data.get('public_address', '')
        signature = request.data.get('signature', '')
        user = authenticate(public_address=public_address, signature=signature)
        if not user:
            return HttpResponse('Unauthorized', status=401)
        login(request, user)
        return JsonResponse(UserSerializer(user).data)


class Logout(APIView):
    def get(self, request):
        logout(request)
        return HttpResponse('Success')


class Nonce(APIView):
    def get(self, request, public_address=''):
        user = User.objects.get_or_create(
            public_address=public_address.lower())[0]
        return JsonResponse(
            {'nonce': user.nonce, 'has_signed_up': bool(user.email) and bool(user.name)})


class UserView(APIView):
    def get(self, request):
        if request.is_logged_in:
            return JsonResponse(UserSerializer(request.current_user).data)
        return HttpResponse('Unauthorized', status=401)


class SettingsView(APIView):
    def post(self, request):
        serializer = SettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        settings = serializer.save()
        user = request.current_user
        user.settings = settings
        user.save()
        return JsonResponse(SettingsSerializer(settings).data)

    def put(self, request):
        user = request.current_user
        settings = user.settings
        serializer = SettingsSerializer(settings, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_settings = serializer.save()
        return JsonResponse(SettingsSerializer(updated_settings).data)


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LanguageSerializer
    queryset = Language.objects.order_by('name')


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RankedSkillSerializer
    queryset = RankedSkill.objects.all()
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend,)
    ordering_fields = ('total_count',)
    ordering = ('-total_count',)
    search_fields = ('normalized_name',)


class UserInfo(APIView):
    def get(self, request, public_address):
        try:
            user = User.objects.get(public_address=public_address.lower())
        except User.DoesNotExist:
            return HttpResponse('Not Found', status=404)

        serializer = UserInfoSerializer(user)
        return JsonResponse(serializer.data)


class UserProfile(APIView):
    def post(self, request, public_address):
        user = request.current_user

        user.profile_touched_manually = True
        user.is_profile_image_dirty = request.data.get('profileDirectoryHash') != str(user.profileDirectoryHash)

        serializer = UserProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user.save_and_clear_skills(request.data.get('skills'))
        user.save_and_clear_languages(request.data.get('languages'))

        user.save()

        notification_client.profile_updated(user.public_address.lower())

        return JsonResponse(UserProfileSerializer(user).data)

    def get(self, request, public_address):
        try:
            user = User.objects.get(public_address=public_address.lower())
        except User.DoesNotExist:
            return JsonResponse({'user': None, 'stats': {}})

        platform = request.GET.get('platform', None)
        additional_filters = {}

        if platform:
            additional_filters.update({'platform': platform})

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
