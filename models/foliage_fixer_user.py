from odoo import fields, models, api


class FoliageFixerUser(models.Model):
    _inherit = 'res.partner'

    firebase_password = fields.Char(string='Firebase Generated Password')
    email = fields.Char(string='email')

    def check_firebase_password(self):
        self.ensure_one()
        for partner in self:
            if not partner.firebase_password:
                return False
            elif partner.firebase_password is None:
                return False
            else:
                return True

    def generate_password(self):
        self.firebase_password = 'generated'
