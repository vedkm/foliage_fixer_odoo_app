import logging
import unittest
from ..services.firebase_auth_provider import FirebaseAuthProvider


class TestFirebaseAuthProvider(unittest.TestCase):

    def setUp(self):
        self.email = 'test@test.com'
        self.password = '123456'
        self.auth = FirebaseAuthProvider()

    def test_sign_in_good_credentials(self):
        logging.info('STARTING TestFirebaseAuthProvider.test_sign_in')
        tokens = self.auth.sign_in(self.email, self.password)
        self.assertIsNotNone(tokens['id_token'])
        logging.info(tokens['id_token'])
        self.assertIsNotNone(tokens['refresh_token'])
        logging.info(tokens['refresh_token'])

    def test_sign_in_bad_credentials(self):
        logging.info('STARTING TestFirebaseAuthProvider.test_sign_in')
        tokens = self.auth.sign_in("wrong", "wrong")
        self.assertIsNone(tokens['id_token'])
        logging.info(tokens['id_token'])
        self.assertIsNone(tokens['refresh_token'])
        logging.info(tokens['refresh_token'])


if __name__ == '__main__':
    unittest.main()
