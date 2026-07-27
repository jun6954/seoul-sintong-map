import unittest
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "supabase/functions/naver-geocode/index.ts"
).read_text()


class NaverGeocodeFunctionTests(unittest.TestCase):
    def test_uses_current_vpc_endpoint_and_keeps_naver_secret_server_side(self):
        self.assertIn("https://maps.apigw.ntruss.com/map-geocode/v2/geocode", SOURCE)
        self.assertIn("NAVER_MAPS_CLIENT_ID", SOURCE)
        self.assertIn("NAVER_MAPS_CLIENT_SECRET", SOURCE)
        self.assertIn("x-ncp-apigw-api-key-id", SOURCE)
        self.assertIn("x-ncp-apigw-api-key", SOURCE)
