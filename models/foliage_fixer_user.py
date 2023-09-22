import random
import string
from cryptography.fernet import Fernet
from odoo import fields, models, api


def _generate_random_string(length):
    letters = string.ascii_letters
    result = ''.join(random.choice(letters) for i in range(length))
    return result


# TODO: set up encryption - figure out how to store the keys
def _encrypt_string(raw_string):
    encrypted = raw_string
    return encrypted


# TODO: set up decryption
def _decrypt_string(encrypted_string):
    decrypted = encrypted_string
    return decrypted


class FoliageFixerUser(models.Model):
    _inherit = 'res.partner'

    firebase_password = fields.Char(string='Firebase Generated Password')
    email = fields.Char(string='email')

    def check_firebase_password(self):
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
        raw = _generate_random_string(length)
        encrypted = _encrypt_string(raw)

        self.firebase_password = encrypted

    def get_firebase_password(self):
        """
        decrypts and returns firebase password
        :return:
        """
        return _decrypt_string(self.firebase_password)
