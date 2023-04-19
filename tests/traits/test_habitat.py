import unittest

from ..setup import test


class TestHabitat(unittest.TestCase):
    def test_habitat_01(self):
        self.assertEqual(
            test("""riparian forest"""),
            [
                {
                    "trait": "habitat",
                    "habitat": "riparian forest",
                    "start": 0,
                    "end": 15,
                },
            ],
        )

    def test_habitat_02(self):
        self.assertEqual(
            test("""subalpine zone"""),
            [
                {
                    "trait": "habitat",
                    "habitat": "subalpine zone",
                    "start": 0,
                    "end": 14,
                }
            ],
        )

    def test_habitat_03(self):
        self.assertEqual(
            test("""Arizona Desert Botanical Garden"""),
            [],
        )
