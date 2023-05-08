import unittest

from tests.setup import test


class TestTownshipRangeSectionPatterns(unittest.TestCase):
    def test_trs_01(self):
        self.assertEqual(
            test("""TRS: NE/14 NW1/4 NW1/4 Nw1/4 S21 T39S R20E"""),
            [
                {
                    "trs": "NE/14 NW1/4 NW1/4 Nw1/4 S21 T39S R20E",
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
                    "trs": "T20N R20W sec 14, 23",
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
                {
                    "trs": "T7N R1E sec 30",
                    "trait": "trs",
                    "start": 0,
                    "end": 19,
                },
            ],
        )
