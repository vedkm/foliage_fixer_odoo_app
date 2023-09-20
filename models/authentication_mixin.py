from odoo import fields, models, api
import requests


class AuthenticationMixin(models.AbstractModel):
    _name = 'foliage_fixer.authentication.mixin'
    _description = 'Authentication Service'

    api_url = fields.Char(string='Api Url')
    token = fields.Char(string='Token')

    def get_token(self):
        return self.token

    def get_new_token(self, email, password):
        try:
            req = requests.post(
                url=self.api_url,
                data={
                    'email': email,
                    'password': password
                }
            )
        except requests.exceptions.HTTPError as e:
            raise e

        self.token = req.json().get('token')
        return req.json().get('token')
