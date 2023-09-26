import unittest
import logging
from odoo import exceptions
from odoo.tests import common


class TestClassification(common.TransactionCase):

    def setUp(self):
        super(TestClassification, self).setUp()
        self.Classification = self.env.get('foliage_fixer.classification')

    def test_01_contains_classification(self):
        test_classification = 'Healthy'
        self.Classification.create({
            'name': test_classification
        })
        contains = self.Classification.contains_classification(test_classification)
        self.assertTrue(contains)

    def test_02_contains_classification(self):
        test_classification = 'Healthy'
        contains = self.Classification.contains_classification(test_classification)
        self.assertFalse(contains)

    def test_01_get_classification(self):
        test_classification = 'Healthy'
        self.Classification.create({
            'name': test_classification
        })
        classification = self.Classification.get_classification_by_name(test_classification)
        self.assertEqual(classification.name, test_classification)

    def test_02_get_classification(self):
        test_classification = 'Healthy'
        classification = self.Classification.get_classification_by_name(test_classification)
        self.assertIsNone(classification)


if __name__ == '__main__':
    unittest.main()
