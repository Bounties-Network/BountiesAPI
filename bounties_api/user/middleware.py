import datetime
from user.backend import get_user
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from uuid import uuid4
import logging
import jwt


logger = logging.getLogger('django')
max_age = 365 * 24 * 60 * 60 * 100


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

    def process_response(self, request, response):
        uuid_cookie = request.COOKIES.get('uuid')
        user_id_cookie = request.COOKIES.get('user_id')
        graphql_authorization_cookie = request.COOKIES.get('authorization')

        if not graphql_authorization_cookie:
            expires = datetime.datetime.strftime(
                datetime.datetime.utcnow() +
                datetime.timedelta(
                    seconds=max_age),
                "%a, %d-%b-%Y %H:%M:%S GMT")
            response.set_cookie(
                'authorization',
                value=jwt.encode({
                    'https://hasura.io/jwt/claims': {
                        'x-hasura-allowed-roles': ['user'],
                        'x-hasura-default-role': 'user',
                        'x-hasura-user-id': request.current_user.id
                    },
                    'exp': expires}, settings.SECRET_KEY, algorithm="HS256"),
                secure=False, httponly=True, expires=expires
            )
        if not uuid_cookie:
            expires = datetime.datetime.strftime(
                datetime.datetime.utcnow() +
                datetime.timedelta(
                    seconds=max_age),
                "%a, %d-%b-%Y %H:%M:%S GMT")
            response.set_cookie(
                'uuid',
                value=uuid4(),
                secure=False,
                httponly=True,
                expires=expires)
        if not user_id_cookie and request.current_user:
            expires = datetime.datetime.strftime(
                datetime.datetime.utcnow() +
                datetime.timedelta(
                    seconds=max_age),
                "%a, %d-%b-%Y %H:%M:%S GMT")
            response.set_cookie(
                'user_id',
                value=request.current_user.id,
                secure=False,
                httponly=True,
                expires=expires)

        return response
