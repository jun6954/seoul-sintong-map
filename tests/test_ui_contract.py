import unittest
from pathlib import Path


HTML = (Path(__file__).resolve().parents[1] / "index.html").read_text()


class UiContractTests(unittest.TestCase):
    def test_address_search_uses_naver_geocoder_and_limits_to_seoul(self):
        self.assertIn("submodules=geocoder", HTML)
        self.assertIn('id="address-input"', HTML)
        self.assertIn("function searchAddress(event)", HTML)
        self.assertIn("function isInsideSeoul(lat, lng)", HTML)
        self.assertIn("서울시 안의 주소만 검색할 수 있습니다.", HTML)

    def test_obsolete_subway_controls_are_removed(self):
        self.assertNotIn("toggleSubway", HTML)
        self.assertNotIn("const STATIONS", HTML)
        self.assertNotIn("지하철역 숨기기", HTML)


if __name__ == "__main__":
    unittest.main()
