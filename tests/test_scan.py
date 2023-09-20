from odoo import exceptions
from odoo.tests import common
import logging
_logger = logging.getLogger(__name__)



class TestScan(common.SingleTransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestScan, self).setUp(*args, **kwargs)

    def test_create_scan(self):
        scan = self.env.get('foliage_fixer.scan').create({
            'image': [(0,0, {
                'name': 'Attachment',
            })]
        })
        self.assertIsNotNone(scan)

    def test_scan(self):
        scan = self.env.get('foliage_fixer.scan').create({
            'image': [(0,0, {
                'name': 'Attachment',
            })]
        })
        scan.scan()
        _logger.info('FINAL SCAN: ' + str(scan.read()))
        self.assertEqual(scan.classification, 'Healthy')