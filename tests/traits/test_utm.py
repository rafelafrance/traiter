import unittest

from tests.setup import test


class TestUTMPatterns(unittest.TestCase):
    def test_utm_01(self):
        self.assertEqual(
            test("""UTM: 12s 359602E 3718689N"""),
            [
                {
                    "utm": "12 S 359602 E 3718689 N",
                    "trait": "utm",
                    "start": 0,
                    "end": 25,
                }
            ],
        )

    def test_utm_02(self):
        self.assertEqual(
            test("""11UQF056380"""),
            [
                {
                    "utm": "11 UQF 056380",
                    "trait": "utm",
                    "start": 0,
                    "end": 11,
                }
            ],
        )
