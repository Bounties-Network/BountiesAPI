import uuid
from user.models import User
# Best approach for now with defunct until other forms are more stable
from eth_account.messages import defunct_hash_message
from web3.auto import w3
import logging


logger = logging.getLogger('django')


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


def logout(request):
    request.session.flush()


def get_user(public_address):
    try:
        return User.objects.get(public_address=public_address.lower())
    except User.DoesNotExist:
        return None
