from user.backend import get_user
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import logging
import jwt


logger = logging.getLogger('django')


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        public_address = request.session.get('public_address', None)
        jwt_token = request.META.get('HTTP_AUTHENTICATION', None)
        if not public_address and jwt_token:
            try:
                payload = jwt.decode(jwt_token, settings.SECRET_KEY)
                public_address = payload.get('public_address', '')
            except Exception as e:
                logger.error(
                    'Decode attempt failed for address: {}, e: {}'.format(
                        public_address, e)
                )

        if public_address:
            request.is_logged_in = True
            request.current_user = get_user(public_address)
        else:
            request.is_logged_in = False
            request.current_user = None
