import unittest

from tests.setup import test


class TestElevation(unittest.TestCase):
    def test_elevation_01(self):
        """It handles metric units."""
        self.assertEqual(
            test(""" Elevation: 1463m """),
            [
                {
                    "trait": "elevation",
                    "elevation": 1463.0,
                    "units": "m",
                    "start": 0,
                    "end": 16,
                },
            ],
        )

    def test_elevation_02(self):
        """It handles a measurement in different units."""
        self.assertEqual(
            test(""" Elev: 782m. (2566 ft) """),
            [
                {
                    "trait": "elevation",
                    "elevation": 782.0,
                    "units": "m",
                    "start": 0,
                    "end": 21,
                },
            ],
        )

    def test_elevation_03(self):
        """It handles a range."""
        traits = test(""" Elev. 9,500-9640 ft. """)
        self.assertEqual(traits[0]["trait"], "elevation")
        self.assertEqual(traits[0]["start"], 0)
        self.assertEqual(traits[0]["end"], 19)
        self.assertEqual(traits[0]["units"], "m")
        self.assertAlmostEqual(traits[0]["elevation"], 2895.6)
        self.assertAlmostEqual(traits[0]["elevation_high"], 2938.272)

    def test_elevation_04(self):
        """Make sure punctuation is not interpreted as numbers."""
        self.assertEqual(
            test(""" alt., 250 m. """),
            [
                {
                    "trait": "elevation",
                    "elevation": 250.0,
                    "units": "m",
                    "start": 0,
                    "end": 12,
                },
            ],
        )

    def test_elevation_05(self):
        self.assertEqual(
            test("""Alto.: 834m/2735ft."""),
            [
                {
                    "trait": "elevation",
                    "elevation": 834.0,
                    "units": "m",
                    "start": 0,
                    "end": 18,
                },
            ],
        )
