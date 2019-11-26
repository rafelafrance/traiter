# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.ovaries_size import OVARY_SIZE


class TestOvariesSize(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            OVARY_SIZE.parse('ovaries = 8x5 mm'),
            [Trait(
                value=[8, 5], units='mm', units_inferred=False,
                start=0, end=16)])

    def test_parse_02(self):
        self.assertEqual(
            OVARY_SIZE.parse('ovary < 1 x 1 mm'),
            [Trait(
                value=[1, 1], units='mm', units_inferred=False,
                start=0, end=16)])

    def test_parse_03(self):
        self.assertEqual(
            OVARY_SIZE.parse('PIT tag #7F7D4D3A36 REMOVAL GRID #7 TRAP 1C'),
            [])

    def test_parse_04(self):
        self.assertEqual(
            OVARY_SIZE.parse(
                'No tail pencil; Mam. gl. enl., 3 emb. L, 5 R. 1 '
                'corpus lut in L ovary, 7 in R.; Enl[?] 8.1 x 3.5'),
            [])

    def test_parse_05(self):
        self.assertEqual(
            OVARY_SIZE.parse(
                'moderate fat, scars 3R, 4L, no embryos '
                '[right ovary listed, left ovary: 4 x 2 mm]'),
            [Trait(
                value=[4, 2], units='mm', units_inferred=False,
                side='left', start=60, end=80)])

    def test_parse_06(self):
        self.assertEqual(
            OVARY_SIZE.parse('Rt Ovary 2.0x3.5mm, Lft Ovary 2.1x4.0mm.'),
            [
                Trait(
                    value=[2, 3.5], units='mm', units_inferred=False,
                    side='rt', start=0, end=18),
                Trait(
                    value=[2.1, 4], units='mm', units_inferred=False,
                    side='lft', start=20, end=39)])

    def test_parse_07(self):
        self.assertEqual(
            OVARY_SIZE.parse('ovaries: 20mm X 12mm, 18mm X 9mm.'),
            [Trait(
                value=[20, 12], units=['mm', 'mm'], units_inferred=False,
                start=0, end=32),
             Trait(
                 value=[18, 9], units=['mm', 'mm'], units_inferred=False,
                 start=0, end=32)])
