import logging
import random
import string
from cryptography.fernet import Fernet


class EncryptionService:
    # TODO: store key in .env
    def __init__(self, key=b'FjArlechHVB_sXzPeeF0c96xHlHMGmkho-HHhSXm6y4='):
        self.f = Fernet(key)

    def generate_random_string(self, length):
        letters = string.ascii_letters
        result = ''.join(random.choice(letters) for i in range(length))
        return result

    def encrypt_string(self, raw_string: str) -> bytes:
        if raw_string is None or not raw_string:
            logging.info('Cannot encrypt empty string.')
            raise ValueError('Cannot encrypt empty string')
        encrypted = raw_string

        encrypted = self.f.encrypt(raw_string.encode())

        return encrypted

    def decrypt_string(self, encrypted_bytes: bytes) -> str:
        if encrypted_bytes is None or not encrypted_bytes:
            logging.info('Cannot encrypt empty string.')
            raise ValueError('Cannot encrypt empty string')
        decrypted = self.f.decrypt(encrypted_bytes).decode()
        return decrypted
