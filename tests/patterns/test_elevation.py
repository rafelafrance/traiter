import unittest

from tests.setup import test


class TestElevation(unittest.TestCase):
    def test_elevation_01(self):
        """It handles metric units."""
        traits = test(""" Elevation: 1463m """)
        self.assertEqual(traits[0]["trait"], "elevation")
        self.assertEqual(traits[0]["start"], 0)
        self.assertEqual(traits[0]["end"], 16)
        self.assertAlmostEqual(traits[0]["elevation"], 1463.0)

    def test_elevation_02(self):
        """It handles a measurement in different units."""
        traits = test(""" Elev: 782m. (2566 ft) """)
        self.assertEqual(traits[0]["trait"], "elevation")
        self.assertEqual(traits[0]["start"], 0)
        self.assertEqual(traits[0]["end"], 21)
        self.assertAlmostEqual(traits[0]["elevation"], 782.0)

    def test_elevation_03(self):
        """It handles a range."""
        traits = test(""" Elev. 9,500-9640 ft. """)
        self.assertEqual(traits[0]["trait"], "elevation")
        self.assertEqual(traits[0]["start"], 0)
        self.assertEqual(traits[0]["end"], 19)
        self.assertAlmostEqual(traits[0]["elevation"], 2895.6)
        self.assertAlmostEqual(traits[0]["elevation_high"], 2938.272)
