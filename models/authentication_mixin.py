import datetime
import logging
from ..services.firebase_auth_provider import FirebaseAuthProvider

from odoo import fields, models, api
from odoo import exceptions
import requests


class AuthenticationMixin(models.AbstractModel):
    """
    Reusable model that provides authentication features to the importing class.
    """
    _name = 'foliage_fixer.authentication.mixin'
    _description = 'Authentication Service'

    auth = FirebaseAuthProvider()

    def get_token(self):

        partner = self.env.user['partner_id']

        id_token, refresh_token, id_token_expiry = self.get_auth_context()

        if id_token_expiry is not None:
            if id_token_expiry > datetime.datetime.now():
                tokens = self.auth.refresh(grant_type='refresh_token', refresh_token=refresh_token)
                id_token = tokens.get['id_token']
                refresh_token = tokens.get['refresh_token']
                expires_in = tokens.get['expires_in']
                self.save_auth_context(id_token, refresh_token, expires_in)

        if id_token is None:
            if partner.check_firebase_password():
                firebase_password = partner.get_firebase_password()
                if firebase_password is None:
                    raise exceptions.MissingError('No firebase password found.')
                tokens = self.auth.sign_in(email=partner.email, password=firebase_password)
                if not tokens:
                    logging.error('Error at authentication_mixin.get_token: sign in failed.')
                    raise exceptions.AccessError('Firebase authentication failed.')
                id_token = tokens['id_token']
                refresh_token = tokens['refresh_token']
                expires_in = tokens['expires_in']
                self.save_auth_context(id_token, refresh_token, expires_in)
            else:
                firebase_password = partner.generate_password()
                if firebase_password is None:
                    raise exceptions.MissingError('Could not generate firebase password.')
                tokens = self.auth.sign_up(email=partner.email, password=firebase_password)
                if not tokens:
                    logging.error('Error at authentication_mixin.get_token: sign in failed after generating password.')
                    raise exceptions.AccessError('Firebase authentication failed.')
                id_token = tokens['id_token']
                refresh_token = tokens['refresh_token']
                expires_in = tokens['expires_in']
                self.save_auth_context(id_token, refresh_token, expires_in)

        return id_token

    # def add_auth_to_request(self, request: requests.request):
    #     token = self.get_token()

    def save_auth_context(self, id_token: str, refresh_token: str, expires_in: str):
        partner = self.env.user['partner_id']
        id_token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=int(expires_in))
        self.with_context(id_token=id_token, refresh_token=refresh_token, id_token_expiry=id_token_expiry)

    def get_auth_context(self):
        partner = self.env.user['partner_id']
        id_token = self.env.context.get('id_token')
        refresh_token = self.env.context.get('refresh_token')
        id_token_expiry = self.env.context.get('id_token_expiry')
        return id_token, refresh_token, id_token_expiry
