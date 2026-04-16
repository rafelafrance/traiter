import unittest

from tests.setup import parse
from traiter.rules.number import Number


class TestNumber(unittest.TestCase):
    def test_number_01(self) -> None:
        self.assertEqual(
            parse(""" 2 3/4 """, numerical=True),
            [
                Number(
                    number=2.75,
                    is_fraction=True,
                    start=0,
                    end=5,
                ),
            ],
        )

    def test_number_02(self) -> None:
        self.assertEqual(
            parse(""" 3/4 """, numerical=True),
            [
                Number(
                    number=0.75,
                    is_fraction=True,
                    start=0,
                    end=3,
                ),
            ],
        )
