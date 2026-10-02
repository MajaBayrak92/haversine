import math
import unittest

from haversine import (
    haversine,
    haversine_unit,
    EARTH_RADIUS_METERS,
    EARTH_RADIUS_KILOMETERS,
    EARTH_RADIUS_MILES,
    EARTH_RADIUS_NAUTICAL_MILES,
)


def approx_equal(actual, expected, tol):
    if math.isnan(expected):
        return math.isnan(actual)
    return abs(actual - expected) <= tol


class TestHaversine(unittest.TestCase):

    def test_identical_points(self):
        self.assertEqual(haversine((51.0, 0.0), (51.0, 0.0)), 0.0)

    def test_one_degree_longitude_at_equator(self):
        d = haversine((0.0, 0.0), (0.0, 1.0), radius=1.0)
        self.assertTrue(approx_equal(d, math.radians(1.0), 1e-9))

    def test_one_degree_latitude_anywhere(self):
        d = haversine((45.0, 0.0), (46.0, 0.0), radius=1.0)
        self.assertTrue(approx_equal(d, math.radians(1.0), 1e-9))

    def test_london_to_paris(self):
        london = (51.5074, -0.1278)
        paris = (48.8566, 2.3522)
        d_km = haversine(london, paris, radius=EARTH_RADIUS_KILOMETERS)
        self.assertTrue(approx_equal(d_km, 343.5, 1.0))

    def test_antipodal_points(self):
        d = haversine((0.0, 0.0), (0.0, 180.0), radius=1.0)
        self.assertTrue(approx_equal(d, math.pi, 1e-9))

    def test_antipodal_off_equator(self):
        d = haversine((45.0, 0.0), (-45.0, 180.0), radius=1.0)
        self.assertTrue(approx_equal(d, math.pi, 1e-9))

    def test_longitude_wraps(self):
        a = (0.0, 179.0)
        b = (0.0, -179.0)
        d = haversine(a, b, radius=1.0)
        self.assertTrue(approx_equal(d, math.radians(2.0), 1e-9))

    def test_known_distance_london_paris_meters(self):
        london = (51.5074, -0.1278)
        paris = (48.8566, 2.3522)
        d = haversine(london, paris)
        self.assertTrue(approx_equal(d, 343556.0, 1000.0))

    def test_symmetric(self):
        a = (40.7128, -74.0060)
        b = (34.0522, -118.2437)
        self.assertEqual(haversine(a, b), haversine(b, a))

    def test_haversine_unit_meters(self):
        d = haversine_unit((0.0, 0.0), (0.0, 1.0), unit="meters")
        self.assertTrue(approx_equal(d, 111195.0, 5.0))

    def test_haversine_unit_kilometers_and_km_alias(self):
        a = (0.0, 0.0)
        b = (0.0, 1.0)
        self.assertEqual(haversine_unit(a, b, "kilometers"), haversine_unit(a, b, "km"))

    def test_haversine_unit_miles(self):
        d = haversine_unit((0.0, 0.0), (0.0, 1.0), unit="miles")
        self.assertTrue(approx_equal(d, 69.097, 0.01))

    def test_haversine_unit_nautical_miles(self):
        d = haversine_unit((0.0, 0.0), (0.0, 1.0), unit="nautical_miles")
        self.assertTrue(approx_equal(d, 60.047, 0.05))

    def test_haversine_unit_unknown_raises_value_error(self):
        with self.assertRaises(ValueError):
            haversine_unit((0.0, 0.0), (1.0, 1.0), unit="furlongs")

    def test_returns_float(self):
        d = haversine((0.0, 0.0), (0.0, 1.0))
        self.assertIsInstance(d, float)

    def test_units_consistent_with_constants(self):
        a = (51.0, 0.0)
        b = (48.0, 2.0)
        self.assertTrue(approx_equal(
            haversine(a, b, EARTH_RADIUS_KILOMETERS) * 1000.0,
            haversine(a, b, EARTH_RADIUS_METERS),
            1e-3,
        ))
        self.assertTrue(approx_equal(
            haversine(a, b, EARTH_RADIUS_MILES) * 1609.344,
            haversine(a, b, EARTH_RADIUS_METERS),
            1e-3,
        ))


if __name__ == "__main__":
    unittest.main()
