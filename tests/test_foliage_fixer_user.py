import logging
from odoo import exceptions
from odoo.tests import common
import random
import string
from cryptography.fernet import Fernet


class TestFoliageFixerUser(common.TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestFoliageFixerUser, self).setUp(*args, **kwargs)
        # test setup here

    def test_01_generate_password(self):
        partner = self.env.get('res.partner').create({'name': 'Test'})
        partner.generate_password()
        self.assertTrue(partner.check_firebase_password())

    def test_check_firebase_password_false(self):
        partner = self.env.get('res.partner').create({'name': 'Test'})
        partner.firebase_password = None
        logging.info('partner: ' + str(partner.read(['firebase_password'])))
        self.assertFalse(partner.check_firebase_password())

    def test_check_firebase_password_true(self):
        partner = self.env.get('res.partner').create({'name': 'Test'})
        partner.firebase_password = 'xxx'
        self.assertTrue(partner.check_firebase_password())

    def test_get_firebase_password(self):
        partner = self.env.get('res.partner').create({'name': 'Test'})
        partner.firebase_password = b'gAAAAABlFEC76RoJxK9HhN1HIUAIYcBys2XbaOuCUEaTMvyXY0cyPUC6F5QWt2SDnpsqZ1NACq6wN81Q5QMqlRcsSa0Y0jT0zg=='
        password = partner.get_firebase_password()
        self.assertIsNotNone(password)
        self.assertTrue(password)
