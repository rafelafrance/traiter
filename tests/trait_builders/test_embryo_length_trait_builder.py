import unittest
from lib.numeric_trait import NumericTrait
from lib.trait_builders.embryo_length_trait_builder \
    import EmbryoLengthTraitBuilder


PAR = None


class TestEmbryoCountTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = EmbryoLengthTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('crown-rump length=13 mm'),
            [NumericTrait(
                value=13, units='mm', units_inferred=False, start=0, end=23)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('Embryo crown-rump length 22'),
            [NumericTrait(
                value=22, units=None, units_inferred=True, start=0, end=27)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse(
                'reproductive data: 4 embryos - 15 mm, crown-rump length'),
            [NumericTrait(
                value=15, units='mm', units_inferred=False, start=21, end=55)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse(', CR (crown-rump length) =7 ;'),
            [NumericTrait(
                value=7, units=None, units_inferred=True, start=6, end=27)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse(', CRL=59 mm; '),
            [NumericTrait(
                value=59, units='mm', units_inferred=False, start=2, end=11)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('pregnant; 1 emb; cr-28'),
            [NumericTrait(
                value=28, units=None, units_inferred=True, start=17, end=22)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('embryos left horn, cr-rump: 23mm.'),
            [NumericTrait(
                value=23, units='mm', units_inferred=False, start=19, end=32)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('4 embs/1R/3L/cr=2mm'),
            [NumericTrait(
                value=2, units='mm', units_inferred=False, start=13, end=19)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('3 embs/2L+2R/cr=X34mm'),
            [NumericTrait(
                value=34, units='mm', units_inferred=False, start=13, end=21)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse(', cr=5x5 ;'),
            [NumericTrait(
                value=[5, 5], units=None, units_inferred=True, start=2, end=8)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('sex=recorded as unknown ; reproductive data=cr=9x8mm'),
            [NumericTrait(
                value=[9, 8], units='mm', units_inferred=False,
                start=44, end=52)])
