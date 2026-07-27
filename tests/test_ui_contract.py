import unittest
from pathlib import Path


HTML = (Path(__file__).resolve().parents[1] / "index.html").read_text()


class UiContractTests(unittest.TestCase):
    def test_address_search_uses_naver_geocoder_and_limits_to_seoul(self):
        self.assertIn('id="address-input"', HTML)
        self.assertIn("function searchAddress(event)", HTML)
        self.assertIn("function requestNaverGeocode(query)", HTML)
        self.assertIn("functions/v1/naver-geocode", HTML)
        self.assertIn("function isInsideSeoul(lat, lng)", HTML)
        self.assertIn("서울시 안의 주소만 검색할 수 있습니다.", HTML)
        self.assertNotIn("naver.maps.Service.geocode", HTML)

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

    def test_dropdown_and_map_click_share_the_selection_and_centering_path(self):
        self.assertIn("naver.maps.Event.addListener(circle, 'click', event => handleMapFeatureClick(event, item))", HTML)
        self.assertIn("naver.maps.Event.addListener(overlay, 'click', event => handleMapFeatureClick(event, item))", HTML)
        self.assertIn("function moveMapTo(position, minimumZoom)", HTML)
        self.assertIn("map.morph(position, Math.max(map.getZoom(), minimumZoom), { duration:700, easing:'easeOutCubic' });", HTML)
        self.assertIn("moveMapTo(new naver.maps.LatLng(project.lat, project.lng), 15);", HTML)

    def test_overlapping_map_features_open_a_picker_and_remove_redundant_notice(self):
        self.assertIn("function handleMapFeatureClick(event, item)", HTML)
        self.assertIn("function openOverlapPicker(coord, candidates)", HTML)
        self.assertIn("function selectOverlapCandidate(index)", HTML)
        self.assertIn("itemContainsPoint(candidate, coord.lat(), coord.lng())", HTML)
        self.assertIn("이 위치에 겹친 사업지", HTML)
        self.assertNotIn("영역을 붉은색으로 표시했습니다.", HTML)

    def test_synced_favorites_use_a_shared_link_and_project_keys(self):
        self.assertIn("function initializeFavorites()", HTML)
        self.assertIn("function toggleFavorite(item, event)", HTML)
        self.assertIn("function projectKey(item)", HTML)
        self.assertIn("function getFavoriteAccessToken()", HTML)
        self.assertIn("functions/v1/shared-favorites", HTML)
        self.assertIn("window.location.hash", HTML)
        self.assertNotIn("signInWithOtp", HTML)
        self.assertNotIn("localStorage", HTML)

    def test_obsolete_subway_controls_are_removed(self):
        self.assertNotIn("toggleSubway", HTML)
        self.assertNotIn("const STATIONS", HTML)
        self.assertNotIn("지하철역 숨기기", HTML)


if __name__ == "__main__":
    unittest.main()
