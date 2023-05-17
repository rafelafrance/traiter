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
                    "lat_long": """40.104905 N, 79.324561 W""",
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
                {
                    "elevation": 1217.0,
                    "trait": "elevation",
                    "start": 29,
                    "end": 40,
                    "units": "m",
                },
            ],
        )

    def test_lat_long_04(self):
        self.assertEqual(
            test("""(Ord Mountains 7.5’ Q.: 34°41'32"N, 116°49'25"W, +1000m)"""),
            [
                {
                    "lat_long": """34° 41' 32" N, 116° 49' 25" W""",
                    "uncertainty": 1000.0,
                    "trait": "lat_long",
                    "start": 24,
                    "end": 56,
                    "units": "m",
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
                    "units": "m",
                }
            ],
        )

    def test_lat_long_06(self):
        self.assertEqual(
            test("""N 33 deg 27' 33", W 111 deg 56' 35","""),
            [
                {
                    "lat_long": """N 33 deg 27' 33", W 111 deg 56' 35\"""",
                    "trait": "lat_long",
                    "start": 0,
                    "end": 35,
                }
            ],
        )

    def test_lat_long_07(self):
        self.assertEqual(
            test("""40.104905N, 79.324561W NAD83."""),
            [
                {
                    "datum": "NAD83",
                    "lat_long": "40.104905 N, 79.324561 W",
                    "trait": "lat_long",
                    "start": 0,
                    "end": 28,
                }
            ],
        )

    def test_lat_long_08(self):
        self.assertEqual(
            test("""33° 53' 31.0" N, -111° 56' 59.9" W"""),
            [
                {
                    "lat_long": """33° 53' 31.0" N, -111° 56' 59.9" W""",
                    "trait": "lat_long",
                    "start": 0,
                    "end": 34,
                }
            ],
        )

    def test_lat_long_09(self):
        self.assertEqual(
            test("""Lat: 41.01102 Long: -75.485306 (WGS-84)"""),
            [
                {
                    "datum": "WGS84",
                    "lat_long": """Lat: 41.01102 Long: -75.485306""",
                    "trait": "lat_long",
                    "start": 0,
                    "end": 39,
                }
            ],
        )

    def test_lat_long_10(self):
        self.assertEqual(
            test("""Lat.: 36° 21'"N Long.: 112° 40'"W"""),
            [
                {
                    "lat_long": """Lat.: 36° 21'" N Long.: 112° 40'" W""",
                    "trait": "lat_long",
                    "start": 0,
                    "end": 33,
                }
            ],
        )

    def test_lat_long_11(self):
        self.assertEqual(
            test("""N 33° 27’ W 111° 56 35" 1200 ft.,"""),
            [
                {
                    "lat_long": '''N 33° 27’ W 111° 56 35"''',
                    "uncertainty": 365.76,
                    "trait": "lat_long",
                    "start": 0,
                    "end": 33,
                    "units": "m",
                }
            ],
        )

    def test_lat_long_12(self):
        """It handles a lat/long range."""
        self.assertEqual(
            test("""Lat. 13.5° - 14°55'S Long. 60.2° - 61°50'W."""),
            [
                {
                    "lat_long": """Lat. 13.5° -14° 55'S Long. 60.2° -61° 50' W.""",
                    "trait": "lat_long",
                    "start": 0,
                    "end": 43,
                }
            ],
        )

    def test_lat_long_13(self):
        self.assertEqual(
            test("""45.01701° N, 118.15694° W Uncertainty: 50 m.; Datum: WGS 84;"""),
            [
                {
                    "lat_long": "45.01701° N, 118.15694° W",
                    "uncertainty": 50.0,
                    "datum": "WGS84",
                    "trait": "lat_long",
                    "start": 0,
                    "end": 59,
                    "units": "m",
                }
            ],
        )

    def test_lat_long_14(self):
        self.assertEqual(
            test("""N41° 50.046’ W087° 54.172’."""),
            [
                {
                    "lat_long": "N41° 50.046’ W087° 54.172’",
                    "trait": "lat_long",
                    "start": 0,
                    "end": 26,
                }
            ],
        )

    def test_lat_long_15(self):
        self.assertEqual(
            test("""27.409578°, -80.397773°"""),
            [
                {
                    "lat_long": "27.409578°, -80.397773°",
                    "trait": "lat_long",
                    "start": 0,
                    "end": 23,
                }
            ],
        )

    def test_lat_long_16(self):
        self.assertEqual(
            test("""Q.: 34°37'17"N, 116°50'15"W,+1000m)"""),
            [
                {
                    "lat_long": """34° 37' 17" N, 116° 50' 15" W""",
                    "trait": "lat_long",
                    "uncertainty": 1000.0,
                    "start": 4,
                    "end": 35,
                    "units": "m",
                }
            ],
        )

    def test_lat_long_17(self):
        self.assertEqual(
            test("""Lat. 29°12.063'N Long. 082°02.005'W Datum: WGS 84."""),
            [
                {
                    "lat_long": "Lat. 29° 12.063' N Long. 082° 02.005' W",
                    "trait": "lat_long",
                    "datum": "WGS84",
                    "start": 0,
                    "end": 49,
                }
            ],
        )
