from authentication.backend import get_user
from django.utils.deprecation import MiddlewareMixin


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id', None)
        if user_id:
            request.is_logged_in = True
            request.current_user = get_user(user_id)
        else:
            request.is_logged_in = False
