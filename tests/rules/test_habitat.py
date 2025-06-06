import unittest

from tests.setup import parse
from traiter.rules.habitat import Habitat


class TestHabitat(unittest.TestCase):
    def test_habitat_01(self):
        self.assertEqual(
            parse("""riparian forest"""),
            [
                Habitat(
                    habitat="riparian forest",
                    start=0,
                    end=15,
                ),
            ],
        )

    def test_habitat_02(self):
        self.assertEqual(
            parse("""subalpine zone"""),
            [
                Habitat(
                    habitat="subalpine zone",
                    start=0,
                    end=14,
                ),
            ],
        )

    def test_habitat_03(self):
        self.assertEqual(
            parse("""Arizona Desert Botanical Garden"""),
            [],
        )

    def test_habitat_04(self):
        self.assertEqual(
            parse(
                """
                park. Habitat: Boggy woodland with a sparce canopy dominated by
                blackgum and larch, and nice herbaceous openings. With:
                """,
            ),
            [
                Habitat(
                    habitat=(
                        "boggy woodland with a sparce canopy dominated by "
                        "blackgum and larch and nice herbaceous openings"
                    ),
                    start=6,
                    end=112,
                ),
            ],
        )

    def test_habitat_05(self):
        self.assertEqual(
            parse("""Riparian/desert scrub."""),
            [
                Habitat(
                    habitat="riparian desert scrub",
                    start=0,
                    end=21,
                ),
            ],
        )
