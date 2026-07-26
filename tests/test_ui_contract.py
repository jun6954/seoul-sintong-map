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

    def test_address_input_suggests_known_project_addresses(self):
        self.assertIn('id="address-suggestions"', HTML)
        self.assertIn("function updateAddressSuggestions()", HTML)
        self.assertIn("function selectAddressSuggestion(index)", HTML)
        self.assertIn("addressSearchItems.push", HTML)
        self.assertIn("서울시 공식 지도 경계가 아직 공개되지 않았습니다.", HTML)

    def test_list_view_and_selected_area_highlight_are_available(self):
        self.assertIn('id="list-view"', HTML)
        self.assertIn("function toggleView()", HTML)
        self.assertIn("function renderList()", HTML)
        self.assertIn("function selectProjectItem(item)", HTML)
        self.assertIn("function highlightZoneCircle(circle)", HTML)
        self.assertIn("strokeColor:'#ef4444'", HTML)

    def test_obsolete_subway_controls_are_removed(self):
        self.assertNotIn("toggleSubway", HTML)
        self.assertNotIn("const STATIONS", HTML)
        self.assertNotIn("지하철역 숨기기", HTML)


if __name__ == "__main__":
    unittest.main()
