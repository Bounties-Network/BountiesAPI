from user.backend import get_user
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import jwt


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        public_address = request.session.get('public_address', None)
        if not public_address:
            jwt_token = request.META.get('HTTP_AUTHENTICATION', '')
            try:
                payload = jwt.decode(jwt_token, settings.SECRET_KEY)
                public_address = payload.get('public_address', '')
            except:
                pass

        if public_address:
            request.is_logged_in = True
            request.current_user = get_user(public_address)
        else:
            request.is_logged_in = False
            request.current_user = None
