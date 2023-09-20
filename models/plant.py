from odoo import fields, models, api


class Plant(models.Model):
    _name = 'foliage_fixer.plant'
    _description = 'Plant'

    name = fields.Char(string="Plant Name")
    family = fields.Char(string="Family")
    scan_ids = fields.One2many(
        comodel_name='foliage_fixer.scan',
        inverse_name='plant_id',
        string='Scans')