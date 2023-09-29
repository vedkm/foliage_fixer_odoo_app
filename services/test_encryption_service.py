import unittest
from ..services import encryption_service


class TestEncryptionService(unittest.TestCase):
    def setUp(self) -> None:
        self.test_f = encryption_service.EncryptionService()

    def test_encrypt_decrypt_string(self):
        raw_string = 'password'
        encrypted = self.test_f.encrypt_string(raw_string)
        self.assertNotEqual(raw_string, encrypted)
        decrypted = self.test_f.decrypt_string(encrypted)
        self.assertEqual(raw_string, decrypted)


if __name__ == '__main__':
    unittest.main()
