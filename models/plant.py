from odoo import fields, models, api


class Plant(models.Model):
    _name = 'foliage_fixer.plant'
    _description = 'Plant'

    name = fields.Char(string="Plant Name", required=True)
    family = fields.Char(string="Family", required=True)
    scan_ids = fields.One2many(
        comodel_name='foliage_fixer.scan',
        inverse_name='plant_id',
        string='Scans')
    classification_ids = fields.Many2many(
        'foliage_fixer.classification',
        'plant_scan_classification_rel',
        'plant_id',
        'classification_id',
        compute='_compute_classification_ids',
        string='Classifications'
    )

    # TODO: currently only shows classifications for current user - may require manually maintaining relation
    @api.depends('scan_ids')
    def _compute_classification_ids(self):
        for plant in self:
            for scan in plant.scan_ids:
                plant.write({'classification_ids': [(4, scan.classification.id)]})
