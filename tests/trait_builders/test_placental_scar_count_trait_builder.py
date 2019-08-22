import unittest
from lib.numeric_trait import NumericTrait
from lib.trait_builders.placental_scar_count_trait_builder \
    import PlacentalScarCountTraitBuilder


PAR = None


class TestPlacentalScarCountTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = PlacentalScarCountTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('no emb; lactating; 7 plac scar'),
            [NumericTrait(value=7, start=19, end=30)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('vagina imperforate; 5 plac scar 3L 2R'),
            [NumericTrait(value=5, left=3, right=2, start=20, end=37)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('3 placental scars, 1L, 2R'),
            [NumericTrait(value=3, left=1, right=2, start=0, end=25)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('4 plac scar'),
            [NumericTrait(value=4, start=0, end=11)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('no placental scars'),
            [NumericTrait(value=0, start=0, end=18)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('2+1=3 placental scars'),
            [NumericTrait(value=3, side1=2, side2=1, start=0, end=21)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('U:P UTMD placental scar 1 + 2'),
            [NumericTrait(value=3, side1=1, side2=2, start=9, end=29)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('uterus enlarged, scarring'),
            [NumericTrait(value='present', start=17, end=25)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('VC, no embs, uterine scars'),
            [NumericTrait(value='present', start=13, end=26)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('plac scar 1L'),
            [NumericTrait(value=1, left=1, start=0, end=12)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('; 4 faint placental scars'),
            [NumericTrait(value=4, start=2, end=25)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('5 plac scars: 3(R)&2(L)'),
            [NumericTrait(value=5, left=2, right=3, start=0, end=22)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('2 placental scars, 0L, 2R'),
            [NumericTrait(value=2, left=0, right=2, start=0, end=25)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('2+1=3 placental scars'),
            [NumericTrait(value=3, side1=2, side2=1, start=0, end=21)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('not breeding, two scars, 1 left, 1 right'),
            [NumericTrait(value=2, left=1, right=1, start=18, end=40)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('placental scars 1 + 1, mam tissue'),
            [NumericTrait(value=2, side1=1, side2=1, start=0, end=21)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('2 P-SCAR R, 1 P-SCAR L'),
            [NumericTrait(value=3, left=1, right=2, start=0, end=22)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse('5 scars: 2lf,3rt'),
            [NumericTrait(value=5, left=2, right=3, start=0, end=16)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse('lactating, P-SCAR-R 3, P-SCAR-L 2'),
            [NumericTrait(value=5, left=2, right=3, start=11, end=33)])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse('1R,0L plac scar'),
            [NumericTrait(value=1, left=0, right=1, start=0, end=15)])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse('3 pac. scars:1(R)&2(L)'),
            [NumericTrait(value=3, left=2, right=1, start=0, end=21)])

    def test_parse_22(self):
        self.assertEqual(
            PAR.parse('plac scar-9; lactating)'),
            [NumericTrait(value=9, start=0, end=11)])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse('VC, no embs, uterine scars'),
            [NumericTrait(value='present', start=13, end=26)])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse('1 lt. plac. scar, 2 rt emb: CR: 16 mm'),
            [NumericTrait(value=3, left=1, right=2, start=0, end=22)])

    def test_parse_25(self):
        self.assertEqual(
            PAR.parse('3+4= 7 placental scars'),
            [NumericTrait(value=7, side1=3, side2=4, start=0, end=22)])

    def test_parse_26(self):
        self.assertEqual(
            PAR.parse('; no embroys or scar'),
            [NumericTrait(value=0, start=2, end=20)])

    def test_parse_27(self):
        self.assertEqual(
            PAR.parse('; 3 prominent placental scars'),
            [NumericTrait(value=3, start=2, end=29)])

    def test_parse_28(self):
        self.assertEqual(
            PAR.parse('VO, pg., 1 embryo (discarded), CRL+28 mm'),
            [])
