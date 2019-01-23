import json

from django.test import TestCase
from django.contrib.auth import SESSION_KEY
from uuid import uuid4

from web3.auto import w3
from eth_account.messages import defunct_hash_message

from user.models import User


public_address = '0xD2C069e6cFcb5256a39ae7A8DaE9d57EE9D5d618'.lower()
private_key = '81a0783ca85e5a3ea544006e1763ee6c3b739b931b6e2898f035eec178d9a957'


class Login(TestCase):
    def test_nonce(self):
        response = self.client.get(f'/auth/{public_address}/nonce/')
        response = json.loads(response.content)
        self.assertEquals(response['has_signed_up'], False)
        self.assertEquals(isinstance(response['nonce'], str), True)

    def test_login_jwt(self):
        nonce = uuid4()
        User.objects.create(
            public_address=public_address,
            nonce=nonce
        )

        message = f'Hi there! Your special nonce: {nonce}'
        message_hash = defunct_hash_message(text=message)
        signed_message = w3.eth.account.signHash(message_hash, private_key=private_key)

        raw_response = self.client.post(f'/auth/login/', data={
            'public_address': public_address,
            'signature': signed_message.signature.hex()
        })

        print(self.client.session[SESSION_KEY])
        response = json.loads(raw_response.content)

        self.assertEqual(raw_response.status_code, 200)
        self.assertEqual(response['public_address'], public_address)
