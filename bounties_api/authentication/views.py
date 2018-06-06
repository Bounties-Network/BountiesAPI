from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from bounties.viewset_mixins import CaseInsensitiveLookupMixin
from authentication.permissions import AuthenticationPermission, IsSelf
from authentication.backend import authenticate, login, logout
from authentication.serializers import UserSerializer
from authentication.models import User
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
        return HttpResponse(user.nonce)


class UserView(APIView):
    def get(self, request):
        if request.is_logged_in:
            return JsonResponse(UserSerializer(request.current_user).data)
        raise Http404()


class UserAddressView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      CaseInsensitiveLookupMixin,
                      viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'public_address'

    def get_permissions(self):
        if self.action == 'update':
            permission_classes = [AuthenticationPermission, IsSelf]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
