import logging

from ..services.encryption_service import EncryptionService
from odoo import fields, models, api


class FoliageFixerUser(models.Model):
    _inherit = ['res.partner']

    firebase_password = fields.Char(string='Firebase Generated Password')
    email = fields.Char(string='email')

    encryption_service = EncryptionService()

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
        raw = self.encryption_service.generate_random_string(length)
        # logging.info("Generated pw: " + raw)
        encrypted = self.encryption_service.encrypt_string(raw)
        # logging.info('Encrypted pw: ' + encrypted.decode())
        #
        self.firebase_password = encrypted.decode()
        # self.firebase_password = raw

    def get_firebase_password(self):
        """
        decrypts and returns firebase password
        :return:
        """
        encrypted = self.firebase_password.encode()
        # logging.info('Encrypted: ' + encrypted.decode())
        decrypted = self.encryption_service.decrypt_string(encrypted)
        # logging.info('Decrypted: ' + decrypted)
        return decrypted

        # return self.firebase_password
