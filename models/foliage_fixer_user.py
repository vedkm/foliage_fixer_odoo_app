from ..services import ff_encryption_service
from odoo import fields, models, api


class FoliageFixerUser(models.Model):
    _inherit = ['res.partner']

    firebase_password = fields.Char(string='Firebase Generated Password')
    email = fields.Char(string='email')

    def check_firebase_password(self):
        '''
        Checks if the current user has a firebase_password.
        :return: true/false
        '''
        self.ensure_one()
        for partner in self:
            if not partner.firebase_password:
                return False
            elif partner.firebase_password is None:
                return False
            else:
                return True

    def generate_password(self, length=10):
        """
        Generates a password of length, encrypts and stores it
        :param length:
        :return:
        """
        raw = ff_encryption_service.generate_random_string(length)
        encrypted = ff_encryption_service.encrypt_string(raw)

        self.firebase_password = encrypted

    def get_firebase_password(self):
        """
        decrypts and returns firebase password
        :return:
        """
        return ff_encryption_service.decrypt_string(self.firebase_password)
