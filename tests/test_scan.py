from odoo import exceptions
from odoo.tests import common
from odoo.tools.profiler import Profiler, make_session, PeriodicCollector
import logging
import unittest

_logger = logging.getLogger(__name__)


class TestScan(common.TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestScan, self).setUp(*args, **kwargs)
        self.plant = self.env.get('foliage_fixer.plant').create({
            'name': 'Plant',
            'family': 'Family'
        })

    def test_create_scan(self):
        logging.info('STARTING TestScan.test_create_scan')
        scan = self.env.get('foliage_fixer.scan').create({
            'image': [(0, 0, {
                'name': 'Attachment',
            })],
            'plant_id': self.plant.id
        })
        self.assertIsNotNone(scan)

    def test_profile_create_scan(self):
        scan_dict = {
            'image': [(0, 0, {
                'name': 'Attachment',
            })],
            'plant_id': self.plant.id
        }
        scan_table = self.env.get('foliage_fixer.scan')
        with Profiler(db='ved_db', collectors=None, profile_session=make_session('create_scan'), description='scan/create'):
            scan_table.create(scan_dict)

    def test_profile_get_scan_by_id(self):
        scan_dict = {
            'image': [(0, 0, {
                'name': 'Attachment',
            })],
            'plant_id': self.plant.id
        }
        scan = self.env.get('foliage_fixer.scan').create(scan_dict)
        scan_table = self.env.get('foliage_fixer.scan')
        with Profiler(db='ved_db', collectors=None, profile_session=make_session('get_scan_by_id'), description='scan/get_by_id'):
            scan_table.browse(scan.id)

    # def test_profile_search_scan_by_name(self):
    #     scan_dict = {
    #         'image': [(0, 0, {
    #             'name': 'Attachment',
    #         })],
    #         'plant_id': self.plant.id
    #     }
    #     scan = self.env.get('foliage_fixer.scan').create(scan_dict)
    #     with Profiler(db='ved_db', collectors=None, profile_session=make_session('get_scan_by_id'), description='scan/get_by_id'):
    #         self.env.get('foliage_fixer.scan').browse(scan.id)

    def test_01_compute_classification_id(self):
        scan = self.env.get('foliage_fixer.scan').create({
            'image': [(0, 0, {
                'name': 'Attachment',
            })],
            'severity': 0,
            'plant_id': self.plant.id
        })
        classification = self.env.get('foliage_fixer.classification').create({
            'name': 'Healthy'
        })
        scan.classification_result = 'Healthy'
        self.assertEqual(scan.classification.id, classification.id)

    def test_02_compute_classification_id(self):
        scan = self.env.get('foliage_fixer.scan').create({
            'image': [(0, 0, {
                'name': 'Attachment',
            })],
            'severity': 0,
            'plant_id': self.plant.id
        })
        scan.classification_result = 'Healthy'
        classification = scan.classification
        self.assertEqual(scan.classification.id, classification.id)

    # def test_scan(self):
    #     logging.info('STARTING TestScan.test_scan')
    #     scan = self.Scan.create({
    #         'image': [(0, 0, {
    #             'name': 'Attachment',
    #         })]
    #     })
    #     scan.scan()
    #     _logger.info('FINAL SCAN: ' + str(scan.read()))
    #     self.assertEqual(scan.classification, 'Healthy')

