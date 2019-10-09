import uuid
from datetime import timezone
from user.models import User
from django.conf import settings
# Best approach for now with defunct until other forms are more stable
from eth_account.messages import defunct_hash_message
from web3.auto import w3
from django.conf import settings
import datetime
import jwt
import logging


logger = logging.getLogger('django')
max_age = 365 * 24 * 60 * 60 * 100


def authenticate(public_address='', signature=''):
    try:
        user = User.objects.get_or_create(
            public_address=public_address.lower())[0]
        message_hash = defunct_hash_message(
            text='Hi there! Your special nonce: {}'.format(user.nonce))
        calculated_public_address = w3.eth.account.recoverHash(
            message_hash, signature=signature)
        user.nonce = uuid.uuid4()
        user.save()
        if calculated_public_address.lower() == public_address.lower():
            return user
    except Exception as e:
        logger.error(
            'Login attempt failed for address: {}, sig: {}'.format(
                public_address, signature), e)
    return None


def login(request, user):
    request.session['public_address'] = user.public_address.lower()
    user.last_logged_in = datetime.datetime.now(timezone.utc)
    user.save()


def loginJWT(request, user):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
    return jwt.encode({'public_address': user.public_address,
                       'https://hasura.io/jwt/claims': {
                           'x-hasura-allowed-roles': ['user'],
                           'x-hasura-default-role': 'user',
                           'x-hasura-user-id': str(user.id)
                       },
                       'exp': expiration}, settings.SECRET_KEY, algorithm="HS256")


def logout(request):
    request.session.flush()


def setLastViewed(request, user):
    user.last_viewed = datetime.datetime.now(timezone.utc)
    user.save()


def get_user(public_address):
    return User.objects.get_or_create(public_address=public_address.lower())[0]
