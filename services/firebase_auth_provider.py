import requests
import logging


class FirebaseAuthProvider:
    # TODO: should be encrypted
    api_key = 'AIzaSyBbbVpZeszVu5jT1hFVCuSvXgTz2hoWYRg'

    def sign_up(self, email, password):
        try:
            resp = requests.post(
                url=f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.api_key}',
                data={
                    'email': email,
                    'password': password,
                    'returnSecureToken': True
                }
            )

            if resp.status_code != 200:
                logging.info('Firebase Response: ' + str(resp.json().get('error')))
                return False

            id_token = resp.json().get('idToken')
            refresh_token = resp.json().get('refreshToken')
            if id_token is None or refresh_token is None:
                return False

            return {
                'id_token': id_token,
                'refresh_token': refresh_token
            }
        except Exception as e:
            logging.info('Exception at firebase_auth_provider.FirebaseAuthProvider.sign_up: ' + e.__repr__())

    def sign_in(self, email, password):
        try:
            resp = requests.post(
                url=f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}',
                data={
                    'email': email,
                    'password': password,
                    'returnSecureToken': True
                }
            )

            if resp.status_code != 200:
                logging.info('Firebase Response: ' + str(resp.json().get('error')))
                return False

            id_token = resp.json().get('idToken')
            refresh_token = resp.json().get('refreshToken')
            if id_token is None or refresh_token is None:
                return False
            return {
                'id_token': id_token,
                'refresh_token': refresh_token
            }
        except Exception as e:
            logging.info('Exception at firebase_auth_provider.FirebaseAuthProvider.sign_in: ' + e.__repr__())

        return False
