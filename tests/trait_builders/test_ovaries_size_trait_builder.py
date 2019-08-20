import unittest
from lib.numeric_trait import NumericTrait
from lib.trait_builders.ovaries_size_trait_builder \
    import OvariesSizeTraitBuilder


PAR = None


class TestOvariesSizeTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = OvariesSizeTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('ovaries = 8x5 mm'),
            [NumericTrait(
                value=[8, 5], units='mm', units_inferred=False,
                start=0, end=16)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('ovary < 1 x 1 mm'),
            [NumericTrait(
                value=[1, 1], units='mm', units_inferred=False,
                start=0, end=16)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('PIT tag #7F7D4D3A36 REMOVAL GRID #7 TRAP 1C'),
            [])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('No tail pencil; Mam. gl. enl., 3 emb. L, 5 R. 1 '
                      'corpus lut in L ovary, 7 in R.; Enl[?] 8.1 x 3.5'),
            [])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('moderate fat, scars 3R, 4L, no embryos '
                      '[right ovary listed, left ovary: 4 x 2 mm]'),
            [NumericTrait(
                value=[4, 2], units='mm', units_inferred=False,
                side='left', start=60, end=80)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('Rt Ovary 2.0x3.5mm, Lft Ovary 2.1x4.0mm.'),
            [
                NumericTrait(
                    value=[2, 3.5], units='mm', units_inferred=False,
                    side='rt', start=0, end=18),
                NumericTrait(
                    value=[2.1, 4], units='mm', units_inferred=False,
                    side='lft', start=20, end=39)])

    def test_parse_07(self):
        self.maxDiff = None
        self.assertEqual(
            PAR.parse('ovaries: 20mm X 12mm, 18mm X 9mm.'),
            [NumericTrait(
                value=[20, 12], units='mm', units_inferred=False,
                start=0, end=32),
             NumericTrait(
                 value=[18, 9], units='mm', units_inferred=False,
                 start=0, end=32)])
