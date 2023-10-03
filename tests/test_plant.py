from odoo import exceptions
from odoo.tests import common
import unittest
from odoo.tools.profiler import Profiler, make_session


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

    def test_profile_search_plants(self):
        plants = self.env.get('foliage_fixer.plant')
        vals_dict = [
            {
                'name': 'Plant 1',
                'family': 'Cherry Tomatoes'
            },
            {
                'name': 'Plant 2',
                'family': 'Cherry Tomatoes'
            },
            {
                'name': 'Plant 3',
                'family': 'Cherry Tomatoes'
            },
            {
                'name': 'Plant 4',
                'family': 'Cherry Tomatoes'
            }
        ]
        with Profiler(db='ved_db', collectors=None, profile_session=make_session('search_plant_by_name'), description='plant/search_name'):
            plants.search([('name', '=', 'Plant 4')])
