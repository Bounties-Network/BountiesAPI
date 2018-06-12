from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from bounties.viewset_mixins import CaseInsensitiveLookupMixin
from authentication.permissions import AuthenticationPermission, IsSelf
from authentication.backend import authenticate, login, logout
from authentication.serializers import UserSerializer
from authentication.models import User
from std_bounties.models import Fulfillment
from django.db.models import Sum, Avg
from django.http import JsonResponse, HttpResponse, Http404


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
    def get(self, request, address=''):
        user = User.objects.get_or_create(public_address=address.lower())[0]
        return JsonResponse({'nonce': user.nonce, 'has_signed_up': bool(user.email)})


class UserView(APIView):
    def get(self, request):
        if request.is_logged_in:
            return JsonResponse(UserSerializer(request.current_user).data)
        raise Http404()


class UserProfile(APIView):
    def get(self, request, address):
        user = User.objects.get(public_address=address.lower())
        user_bounties = user.bounty_set
        user_fulfillments = user.fulfillment_set
        user_reviews = user.reviews
        user_reviewees = user.reviewees

        awarded = Fulfillment.objects.filter(accepted=True, bounty__user=user).aggregate(Sum('usd_price'))
        earned = user_fulfillments.filter(accepted=True).aggregate(Sum('usd_price'))
        issuer_ratings_given = user_reviews.filter(fulfillment_review__isnull=False).aggregate(Avg('rating'))
        issuer_ratings_received = user_reviewees.filter(issuer_review__isnull=False).aggregate(Avg('rating'))
        fulfiller_ratings_given = user_reviews.filter(issuer_review__isnull=False).aggregate(Avg('rating'))
        fulfiller_ratings_received = user_reviewees.filter(fulfillment_review__isnull=False).aggregate(Avg('rating'))
        issuer_fulfillment_acceptance = None if not Fulfillment.objects.filter(bounty__user=user).count() else (Fulfillment.objects.filter(accepted=True, bounty__user=user).count() / Fulfillment.objects.filter(bounty__user=user).count())
        fulfiller_fulfillment_acceptance = None if not user_fulfillments.count() else (user_fulfillments.count(accepted=True) / user_fulfillments.count())

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
            'total_fulfillments': user_fulfillments.count()
        }
        serializer = UserSerializer(user)

        return JsonResponse({'user': serializer.data, 'stats': profile_stats})


class UserAddressView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      CaseInsensitiveLookupMixin,
                      viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'public_address'

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [AuthenticationPermission, IsSelf]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
