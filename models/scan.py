from odoo import fields, models, api


class Scan(models.Model):
    _name = 'foliage_fixer.scan'
    _description = 'Scan'

    image = fields.Many2many('ir.attachment', string='Image')

    classification = fields.Char(string='Classification')
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
