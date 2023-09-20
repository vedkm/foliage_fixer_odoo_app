from odoo import fields, models, api


class FoliageFixerUser(models.Model):
    _inherit = 'res.partner'

    firebase_password = fields.Char(string='Firebase Generated Password')
    email = fields.Char(string='email', required=True)


    def check_firebase_password(self):
        return self.firebase_password is not None

    def generate_password(self):
        return True