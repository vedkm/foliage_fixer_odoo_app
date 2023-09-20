from odoo import fields, models, api
import requests


class Scan(models.Model):
    _name = 'foliage_fixer.scan'
    _description = 'Scan'
    _inherit = ['foliage_fixer.authentication.mixin']

    image = fields.Many2many('ir.attachment', string='Image')

    classification = fields.Char(string='Classification', compute='scan')
    severity = fields.Float(string='Severity')
    severity_category = fields.Selection([
        ('Healthy', 'green'),
        ('Slightly Unhealthy', 'yellow'),
        ('Unhealthy', 'red')
    ], string='Severity Category',
        compute='_compute_severity_category',
        store=True)

    plant_id = fields.Many2one('foliage_fixer.plant',
                               string='Plant')
    plant_name = fields.Char(string='Plant Name', related='plant_id.name')

    # @api.model
    # def create(self, vals_list):
    #     res = super(Scan, self).create(vals_list)
    #     return res

    @api.depends('severity')
    def _compute_severity_category(self):
        for scan in self:
            if scan.severity < 0.15:
                scan.severity_category = 'Healthy'
            if 0.15 <= scan.severity < 0.65:
                scan.severity_category = 'Slightly Unhealthy'
            if 0.65 <= scan.severity < 1:
                scan.severity_category = 'Unhealthy'

    @api.depends('image')
    def scan(self):

        for scan in self:

            scan.api_url = 'https://foliagefixerbackend-5niucyg5nq-ue.a.run.app/loginn'

            resp = requests.post(
                url='https://foliagefixerbackend-5niucyg5nq-ue.a.run.app/classify',
                data={
                    'image': scan.image
                },
                headers={
                    'authorization': scan.get_new_token(email='test@test.com', password='123456')
                }
            )

            scan.classification = resp.json().get('classification')
            scan.severity = resp.json().get('severity')
