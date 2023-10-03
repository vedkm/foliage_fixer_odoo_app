import unittest
from ..services.scanner_service import TomatoScannerService
import responses
from odoo.tests import common
from requests import HTTPError


class TestScannerService(common.SingleTransactionCase):
    @responses.activate
    def test_successful_scan(self):
        scanner = TomatoScannerService(api_url="https://example.com/classify")
        rsp = responses.post(
            "https://example.com/classify",
            json={
                "classification": "Healthy",
                "severity": 0
            },
            status=200
        )
        result = scanner.scan(None,"token")
        self.assertDictEqual(result, {
            "classification": "Healthy",
            "severity": 0
        })

    @responses.activate
    def test_unauthenticated_scan(self):
        scanner = TomatoScannerService(api_url="https://example.com/classify")
        rsp = responses.post(
            "https://example.com/classify",
            json={
                "error": "UNAUTHENTICATED"
            },
            status=401
        )
        result = scanner.scan(None, "token")
        self.assertRaises(HTTPError)
        self.assertIsNone(result)

    @responses.activate
    def test_bad_request_scan(self):
        scanner = TomatoScannerService(api_url="https://example.com/classify")
        rsp = responses.post(
            "https://example.com/classify",
            json={
                "error": "BAD REQUEST"
            },
            status=400
        )
        result = scanner.scan(None, "token")
        # self.assertRaises(HTTPError)
        self.assertIsNone(result)
