import unittest

from tests.setup import test


class TestLatLongPatterns(unittest.TestCase):
    def test_lat_long_01(self):
        self.assertEqual(
            test("""Grassland, GPS 30° 49’ 27’ N, 99" 15' 22 W May"""),
            [
                {"habitat": "grassland", "trait": "habitat", "start": 0, "end": 9},
                {
                    "lat_long": """30° 49’ 27’ N, 99" 15' 22 W""",
                    "trait": "lat_long",
                    "start": 11,
                    "end": 42,
                },
            ],
        )

    def test_lat_long_02(self):
        self.assertEqual(
            test("""floodplain wetland. 40.104905N, 79.324561W NAD83"""),
            [
                {
                    "end": 18,
                    "habitat": "floodplain wetland",
                    "start": 0,
                    "trait": "habitat",
                },
                {
                    "lat_long": """40.104905N, 79.324561W""",
                    "trait": "lat_long",
                    "datum": "NAD83",
                    "start": 20,
                    "end": 48,
                },
            ],
        )

    def test_lat_long_03(self):
        self.assertEqual(
            test("""32° 19.517' N 110° 40.242' W Elev: 1217m"""),
            [
                {
                    "lat_long": """32° 19.517' N 110° 40.242' W""",
                    "trait": "lat_long",
                    "start": 0,
                    "end": 28,
                },
                {"elevation": 1217.0, "trait": "elevation", "start": 29, "end": 40},
            ],
        )

    def test_lat_long_04(self):
        self.assertEqual(
            test("""(Ord Mountain 7.5’ Q.: 34°41'32"N, 116°49'25"W, +1000m)"""),
            [
                {
                    "lat_long": """34° 41'32"N, 116° 49'25"W""",
                    "uncertainty": 1000.0,
                    "trait": "lat_long",
                    "start": 23,
                    "end": 54,
                }
            ],
        )

    def test_lat_long_05(self):
        self.assertEqual(
            test("""43.963272° N, 113.446226° W Uncertainty: 100 m."""),
            [
                {
                    "lat_long": """43.963272° N, 113.446226° W""",
                    "uncertainty": 100.0,
                    "trait": "lat_long",
                    "start": 0,
                    "end": 47,
                }
            ],
        )
