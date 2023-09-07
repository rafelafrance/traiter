import unittest

from tests.setup import test


class TestTRSPatterns(unittest.TestCase):
    def test_trs_01(self):
        self.assertEqual(
            test("""TRS: NE/14 NW1/4 NW1/4 Nw1/4 S21 T39S R20E"""),
            [
                {
                    "trs": "present",
                    "trait": "trs",
                    "start": 0,
                    "end": 42,
                },
            ],
        )

    def test_trs_02(self):
        self.assertEqual(
            test("""TRS: T20N R20W sec 14, 23;"""),
            [
                {
                    "trs": "present",
                    "trait": "trs",
                    "start": 0,
                    "end": 25,
                },
            ],
        )

    def test_trs_03(self):
        self.assertEqual(
            test("""TRS: T7N R1E sec 30 39.10010 -112.298611"""),
            [
                {"trs": "present", "trait": "trs", "start": 0, "end": 19},
                {
                    "lat_long": "39.10010 -112.298611",
                    "trait": "lat_long",
                    "start": 20,
                    "end": 40,
                },
            ],
        )

    def test_trs_04(self):
        self.assertEqual(
            test("""T22N, R27E, S36."""),
            [
                {
                    "trs": "present",
                    "trait": "trs",
                    "start": 0,
                    "end": 16,
                },
            ],
        )

    def test_trs_05(self):
        self.assertEqual(
            test("""Lehigh Acres T44S, R26E, S25, NEZ Shallow water"""),
            [
                {
                    "trs": "present",
                    "trait": "trs",
                    "start": 13,
                    "end": 29,
                },
            ],
        )

    def test_trs_06(self):
        self.assertEqual(
            test("""Sec 20, T33N, R7E,"""),
            [
                {
                    "trs": "present",
                    "trait": "trs",
                    "start": 0,
                    "end": 18,
                },
            ],
        )

    def test_trs_07(self):
        self.assertEqual(
            test("""NW 32nd Avenue"""),
            [],
        )

    def test_trs_08(self):
        self.assertEqual(
            test("""Sec.33 T37N,"""),
            [
                {
                    "trs": "present",
                    "trait": "trs",
                    "start": 0,
                    "end": 12,
                },
            ],
        )
