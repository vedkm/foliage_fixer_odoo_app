import logging
import unittest
import responses

from odoo.tests import common


class MockAuthProvider:
    def __init__(self, api_key='key'):
        self.api_key = api_key

    def sign_up(self, email, password):
        return {
            'id_token': 'token',
            'refresh_token': 'refresh',
            'expires_in': 'expires'
        }

    def sign_in(self, email, password):
        return {
            'id_token': 'token',
            'refresh_token': 'refresh',
            'expires_in': 'expires'
        }

    def refresh(self, grant_type, refresh_token):
        return {
            'id_token': 'token',
            'refresh_token': 'refresh',
            'expires_in': 'expires'
        }


class TestAuthenticationMixin(common.TransactionCase):
    def setUp(self):
        super(TestAuthenticationMixin, self).setUp()
        self.api_url = 'https://foliagefixerbackend-5niucyg5nq-ue.a.run.app/loginn'
        logging.info(str(self.api_url))

    @unittest.skip
    def test_get_token(self):
        logging.info('STARTING test_authentication_mixin.test_get_token')
        auth = self.env.get('foliage_fixer.authentication.mixin')
        token = auth.get_token(auth_provider=MockAuthProvider())
        logging.info('TOKEN: ' + str(token))
        self.assertIsNotNone(token)
