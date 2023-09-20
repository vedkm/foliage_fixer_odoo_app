from odoo import exceptions
from odoo.tests import common


class TestFoliageFixerUser(common.TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestFoliageFixerUser, self).setUp(*args, **kwargs)
        #test setup here



    def test_01_generate_password(self):
        partner = self.env.get('res.partner').create({'name': 'Test'})
        before = partner.firebase_password
        after = partner.generate_password()
        self.assertNotEqual(before, after)

    def test_check_firebase_password(self):
        partner = self.env.get('res.partner').create({'name': 'Test'})
        partner.firebase_password = None
        self.assertTrue(partner.check_firebase_password())
