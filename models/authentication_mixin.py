import logging
from ..services.firebase_auth_provider import FirebaseAuthProvider

from odoo import fields, models, api
from odoo import exceptions
import requests


class AuthenticationMixin(models.AbstractModel):
    _name = 'foliage_fixer.authentication.mixin'
    _description = 'Authentication Service'

    auth = FirebaseAuthProvider()

    def get_token(self):

        partner = self.env.get('res.partner').browse([self.env.user['id']])

        # id_token = self.env.context.get('foliage_fixer_api_token')
        id_token = None

        if id_token is None:
            if partner.check_firebase_password():
                tokens = self.auth.sign_in(email=partner.email, password=partner.firebase_password)
                if not tokens:
                    logging.error('Error at authentication_mixin.get_token: sign in failed.')
                    raise exceptions.AccessError('Firebase authentication failed.')
                id_token = tokens['id_token']
                refresh_token = tokens['refresh_token']
                partner.with_context(id_token=id_token, refresh_token=refresh_token)
            else:
                partner.generate_password()
                tokens = self.auth.sign_up(email=partner.email, password=partner.firebase_password)
                if not tokens:
                    logging.error('Error at authentication_mixin.get_token: sign in failed after generating password.')
                    raise exceptions.AccessError('Firebase authentication failed.')
                id_token = tokens['id_token']
                refresh_token = tokens['refresh_token']
                partner.with_context(id_token=id_token, refresh_token=refresh_token)

        return id_token
