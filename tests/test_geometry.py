import unittest

from scripts.fetch_general_projects import geometry_center, transform_geometry


class GeometryTests(unittest.TestCase):
    def test_transforms_seoul_portal_polygon_to_wgs84(self):
        shape = {
            "type": "Polygon",
            "coordinates": [[[200000, 450000], [200100, 450000], [200100, 450100], [200000, 450100], [200000, 450000]]],
        }

        geometry = transform_geometry(shape)

        self.assertEqual(geometry["type"], "Polygon")
        longitude, latitude = geometry["coordinates"][0][0]
        self.assertGreater(longitude, 126)
        self.assertGreater(latitude, 37)

    def test_uses_centroid_of_largest_polygon(self):
        geometry = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[126.0, 37.0], [126.0, 37.1], [126.1, 37.1], [126.1, 37.0], [126.0, 37.0]]],
                [[[127.0, 38.0], [127.0, 38.4], [127.4, 38.4], [127.4, 38.0], [127.0, 38.0]]],
            ],
        }

        latitude, longitude = geometry_center(geometry)

        self.assertAlmostEqual(latitude, 38.2, places=5)
        self.assertAlmostEqual(longitude, 127.2, places=5)


if __name__ == "__main__":
    unittest.main()
