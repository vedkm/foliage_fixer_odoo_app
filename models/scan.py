import base64

import odoo.exceptions
from odoo import fields, models, api
import requests
import logging
from odoo.exceptions import ValidationError, UserError
from ..services.scanner_service import TomatoScannerService
from ..services.firebase_auth_provider import FirebaseAuthProvider


# from dotenv import load_dotenv

class Scan(models.Model):
    _name = 'foliage_fixer.scan'
    _description = 'Scan'
    # TODO: in hindsight, I really don't like this. Makes future development more difficult
    _inherit = 'foliage_fixer.authentication.mixin'

    name = fields.Char(string='Name', compute='_compute_name')

    image = fields.Many2many('ir.attachment', string='Image Attachment', required=True)
    # not sure if this will affect performance
    image_binary = fields.Binary(string='Image', related='image.datas', store=False)

    classification = fields.Many2one('foliage_fixer.classification', string='Classification ID',
                                     compute='_compute_classification_id')
    # classification = fields.Char(string='Classification', compute='scan', readonly=True, store=True)
    classification_name = fields.Char(string='Classification', related='classification.name')
    classification_result = fields.Char(string='Classification API Result')

    severity = fields.Float(string='Severity', readonly=True)
    severity_category = fields.Selection([
        ('green', 'Healthy'),
        ('yellow', 'Slightly Unhealthy'),
        ('red', 'Unhealthy')
    ], string='Severity Category',
        compute='_compute_severity_category',
        store=True, readonly=True)

    plant_id = fields.Many2one('foliage_fixer.plant',
                               string='Plant', required=True)
    plant_name = fields.Char(string='Plant Name', related='plant_id.name')

    @api.depends('severity')
    def _compute_severity_category(self):
        for scan in self:
            if scan.severity < 15:
                scan.severity_category = 'green'
            if 15 <= scan.severity < 80:
                scan.severity_category = 'yellow'
            if 80 <= scan.severity <= 100:
                scan.severity_category = 'red'

    @api.constrains('severity')
    def _check_severity(self):
        for scan in self:
            if scan.severity < 0 or scan.severity > 100:
                raise ValidationError('Severity must be a float between 0 and 100.')

    @api.depends('plant_id', 'classification_result', 'severity')
    def _compute_name(self):
        for scan in self:
            scan.name = f"{scan.plant_name}: {scan.classification_name}"

    @api.depends('classification_result')
    def _compute_classification_id(self):
        for scan in self:
            classification_table = self.env.get('foliage_fixer.classification')
            classification_record = classification_table.get_classification_by_name(scan.classification_result)
            if classification_record is None:
                classification_record = classification_table.create({
                    'name': scan.classification_result
                })
            scan.classification = classification_record

    def scan(self, scanner_service=TomatoScannerService(), auth_provider=FirebaseAuthProvider()):
        self.ensure_one()
        for scan in self:
            id_token = scan.get_token(auth_provider=auth_provider)
            if not id_token:
                logging.info('Error at model scan.get_token: authentication failed - no id token.')
                return None

            image_data = scan.image.datas
            decoded = base64.b64decode(image_data)

            scan_results = scanner_service.scan(decoded, id_token)
            scan.classification_result = scan_results.get('classification')
            scan.severity = scan_results.get('severity')
            # compute isn't executed after automated action
            self._compute_severity_category()
