# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class foliage_fixer_app(models.Model):
#     _name = 'foliage_fixer_app.foliage_fixer_app'
#     _description = 'foliage_fixer_app.foliage_fixer_app'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
