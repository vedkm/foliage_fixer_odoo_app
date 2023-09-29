from odoo import exceptions
from odoo.tests import common
import unittest


class TestPlant(common.SingleTransactionCase):
    def setUp(self):
        pass

    def test_create_plant(self):
        expected = {
            'name': 'Tomato 1',
            'family': 'Tomatoes'
        }

        tomato = self.env['foliage_fixer.plant'].create(expected)

        got = {
            'name': tomato.name,
            'family': tomato.family
        }

        self.assertDictEqual(expected, got)

    # def test_compute_classification_ids(self):
    #     [self.assertEqual() for plant.classification_ids in ]


# if __name__ == '__main__':
#     unittest.main()