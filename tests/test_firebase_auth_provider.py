import logging
import unittest
from ..services.firebase_auth_provider import FirebaseAuthProvider
import responses


class TestFirebaseAuthProvider(unittest.TestCase):

    def setUp(self):
        self.email = 'test@test.com'
        self.password = '123456'
        self.auth = FirebaseAuthProvider(api_key='key')

    @responses.activate
    def test_sign_in_good_credentials(self):
        logging.info('STARTING TestFirebaseAuthProvider.test_sign_in')
        resp = responses.post(
            f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.auth.api_key}',
            json={
                'idToken': 'token',
                'refreshToken': 'refresh',
                'expiresIn': 'expires'
            },
            status=200
        )
        tokens = self.auth.sign_in(self.email, self.password)
        self.assertEqual(tokens['id_token'], 'token')
        self.assertEqual(tokens['refresh_token'], 'refresh')
        self.assertEqual(tokens['expires_in'], 'expires')

    @responses.activate
    def test_sign_in_bad_credentials(self):
        logging.info('STARTING TestFirebaseAuthProvider.test_sign_in')
        resp = responses.post(
            f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.auth.api_key}',
            json={
                'ERROR': 'UNAUTHENTICATED'
            },
            status=401
        )
        tokens = self.auth.sign_in('wrong', 'wrong')
        self.assertIsNone(tokens)


if __name__ == '__main__':
    unittest.main()
