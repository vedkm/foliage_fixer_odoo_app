from odoo import fields, models, api


class Classification(models.Model):
    _name = 'foliage_fixer.classification'
    _description = 'Classification'

    name = fields.Char(string="Name")
    _sql_constraints = [
        ('name', 'unique (name)', 'The field must be unique!')
    ]

    def contains_classification(self, classification_name: str):
        if self.search_count([('name', '=', classification_name)]) > 0:
            return True

        return False

    def get_classification_by_name(self, name: str):
        classification = self.search([('name', '=', name)])
        if not classification:
            return None
        return classification
