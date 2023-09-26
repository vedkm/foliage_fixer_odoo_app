import logging
import unittest

from odoo.tests import common


class TestAuthenticationMixin(common.TransactionCase):
    def setUp(self):
        super(TestAuthenticationMixin, self).setUp()
        self.api_url = 'https://foliagefixerbackend-5niucyg5nq-ue.a.run.app/loginn'
        logging.info(str(self.api_url))

    @unittest.skip
    def test_get_token(self):
        logging.info('STARTING test_authentication_mixin.test_get_token')
        auth = self.env.get('foliage_fixer.authentication.mixin')
        token = auth.get_token()
        logging.info('TOKEN: ' + str(token))
        self.assertIsNotNone(token)
