import logging

import cryptography.exceptions

from ..services.encryption_service import EncryptionService
from odoo import fields, models, api


class FoliageFixerUser(models.Model):
    _inherit = ['res.partner']

    firebase_password = fields.Char(string='Firebase Generated Password')
    email = fields.Char(string='email')

    encryption_service = EncryptionService()

    def check_firebase_password(self) -> bool:
        """
        Checks if the current user has a firebase_password.
        :return: true/false
        """
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
        :return: generated password if successful or None if encryption fails
        """
        raw = self.encryption_service.generate_random_string(length)
        encrypted = self.encryption_service.encrypt_string(raw)
        if encrypted is None:
            return None
        self.firebase_password = encrypted.decode()
        return raw

    def get_firebase_password(self):
        """
        reads firebase password from db, decrypts it and returns the string
        :return: firebase password
        """
        encrypted = self.firebase_password.encode()
        decrypted = self.encryption_service.decrypt_string(encrypted)
        if decrypted is None:
            return None
        return decrypted
