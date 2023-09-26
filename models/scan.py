import base64

import odoo.exceptions
from odoo import fields, models, api
import requests
import logging
from odoo.exceptions import ValidationError, UserError


class Scan(models.Model):
    _name = 'foliage_fixer.scan'
    _description = 'Scan'
    _inherit = 'foliage_fixer.authentication.mixin'

    name = fields.Char(string='Name', compute='_compute_name')

    image = fields.Many2many('ir.attachment', string='Image Attachment', required=True)
    # not sure if this will affect performance
    image_binary = fields.Binary(string='Image', related='image.datas', store=False)

    classification = fields.Char(string='Classification', compute='scan', readonly=True, store=True)
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

    # @api.model
    # def create(self, vals_list):
    #     res = super(Scan, self).create(vals_list)
    #     return res

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

    @api.depends('plant_id', 'classification', 'severity')
    def _compute_name(self):
        for scan in self:
            scan.name = f"{scan.plant_name}: {scan.classification}"

    def scan(self):
        self.ensure_one()
        for scan in self:
            id_token = scan.get_token()
            if not id_token:
                logging.info('Error at model scan.get_token: authentication failed - no id token.')
                return None

            image_data = scan.image.datas
            decoded = base64.b64decode(image_data)

            try:
                resp = requests.post(
                    url='https://foliagefixerbackend-5niucyg5nq-ue.a.run.app/classify',
                    files={
                        'image': decoded
                    },
                    headers={
                        'authorization': id_token
                    }
                )
                logging.info('RESPONSE: ' + str(resp.json()))
                scan.classification = resp.json().get('classification')
                scan.severity = resp.json().get('severity')
                # compute isn't executed after automated action
                self._compute_severity_category()
            except requests.HTTPError as e:
                logging.error(f'HTTP error from scan API: {str(e)}')
                raise UserError('Failed to scan. Received error from scan API.')
            except requests.exceptions.RequestException as e:
                logging.error('Error at scan request: ' + str(e))
                raise UserError('Failed to scan.')
            except Exception as e:
                logging.error(e)
