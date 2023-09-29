import logging
import random
import string

import cryptography.exceptions
from cryptography.fernet import Fernet


class EncryptionService:
    # TODO: store key in .env
    def __init__(self, key=b'FjArlechHVB_sXzPeeF0c96xHlHMGmkho-HHhSXm6y4='):
        self.f = Fernet(key)

    def generate_random_string(self, length: int):
        """
        Generates a random string of length
        :param length: int
        :return: random string
        """
        letters = string.ascii_letters
        result = ''.join(random.choice(letters) for i in range(length))
        return result

    def encrypt_string(self, raw_string: str) -> bytes or None:
        """
        Encrypts string and returns it as bytes
        :param raw_string: plaintext string
        :return: bytes if successful, None if encryption fails
        """
        if raw_string is None or not raw_string:
            logging.info('Cannot encrypt empty string.')
            raise ValueError('Cannot encrypt empty string')
        try:
            encrypted = self.f.encrypt(raw_string.encode())
        except cryptography.exceptions.InvalidKey as e:
            return None
        return encrypted

    def decrypt_string(self, encrypted_bytes: bytes) -> str or None:
        """
        Decrypts encrypted bytes and returns the decrypted string
        :param encrypted_bytes:
        :return: decrypted string if successful, None if unsuccessful
        """
        if encrypted_bytes is None or not encrypted_bytes:
            logging.info('Cannot encrypt empty string.')
            raise ValueError('Cannot encrypt empty string')

        try:
            decrypted = self.f.decrypt(encrypted_bytes).decode()
        except cryptography.exceptions.InvalidKey as e:
            logging.error(str(e))
            return None
        return decrypted
