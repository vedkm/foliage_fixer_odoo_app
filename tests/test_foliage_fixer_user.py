from odoo import exceptions
from odoo.tests import common


class TestFoliageFixerUser(common.TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestFoliageFixerUser, self).setUp(*args, **kwargs)
        #test setup here



    def test_01_generate_password(self):
        before = self.firebase_password
        assert True

    def test_check_firebase_password(self):
        user = self.env.ref('res.partner')
        self.User = user
        self.assertFalse(self.User.firebase_password)
