import requests
import logging

from odoo.exceptions import UserError

# from firebase_auth_provider import FirebaseAuthProvider


class TomatoScannerService:
    def __init__(self, api_url='https://foliagefixerbackend-5niucyg5nq-ue.a.run.app/classify'):
        self.api_url = api_url

    def scan(self, image, id_token):
        try:
            resp = requests.post(
                url=self.api_url,
                files={
                    'image': image
                },
                headers={
                    'authorization': id_token
                }
            )
            logging.info('RESPONSE: ' + str(resp.json()))

            classification_result = resp.json().get('classification')
            severity = resp.json().get('severity')
            return {
                'classification': classification_result,
                'severity': severity
            }
        except requests.HTTPError as e:
            logging.error(f'HTTP error from scan API: {str(e)}')
            raise UserError('Failed to scan. Received error from scan API.')
        except requests.exceptions.RequestException as e:
            logging.error('Error at scan request: ' + str(e))
            raise UserError('Failed to scan.')
        except Exception as e:
            logging.error(e)
