from user.backend import get_user
from django.utils.deprecation import MiddlewareMixin


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        public_address = request.session.get('public_address', None)
        if public_address:
            request.is_logged_in = True
            request.current_user = get_user(public_address)
        else:
            request.is_logged_in = False
            request.current_user = None
