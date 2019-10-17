import unittest
from pylib.numeric_trait import NumericTrait
from pylib.parsers.embryo_length import EMBRYO_LENGTH


class TestEmbryoCount(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('crown-rump length=13 mm'),
            [NumericTrait(
                value=13, units='mm', units_inferred=False, start=0, end=23)])

    def test_parse_02(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('Embryo crown-rump length 22'),
            [NumericTrait(
                value=22, units=None, units_inferred=True, start=0, end=27)])

    def test_parse_03(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(
                'reproductive data: 4 embryos - 15 mm, crown-rump length'),
            [NumericTrait(
                value=15, units='mm', units_inferred=False, start=21, end=55)])

    def test_parse_04(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(', CR (crown-rump length) =7 ;'),
            [NumericTrait(
                value=7, units=None, units_inferred=True, start=6, end=27)])

    def test_parse_05(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(', CRL=59 mm; '),
            [NumericTrait(
                value=59, units='mm', units_inferred=False, start=2, end=11)])

    def test_parse_06(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('pregnant; 1 emb; cr-28'),
            [NumericTrait(
                value=28, units=None, units_inferred=True, start=17, end=22)])

    def test_parse_07(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('embryos left horn, cr-rump: 23mm.'),
            [NumericTrait(
                value=23, units='mm', units_inferred=False, start=19, end=32)])

    def test_parse_08(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('4 embs/1R/3L/cr=2mm'),
            [NumericTrait(
                value=2, units='mm', units_inferred=False, start=13, end=19)])

    def test_parse_09(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('3 embs/2L+2R/cr=X34mm'),
            [NumericTrait(
                value=34, units='mm', units_inferred=False, start=13, end=21)])

    def test_parse_10(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(', cr=5x5 ;'),
            [NumericTrait(
                value=[5, 5], units=None, units_inferred=True,
                start=2, end=8)])

    def test_parse_11(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(
                'sex=recorded as unknown ; reproductive data=cr=9x8mm'),
            [NumericTrait(
                value=[9, 8], units='mm', units_inferred=False,
                start=44, end=52)])

    def test_parse_12(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(
                'reproductive data=Embryos: 2 (1 resorbing) R, 3 Left, '
                'crown-rump length, 36 mm.'),
            [NumericTrait(
                value=36, units='mm', units_inferred=False,
                start=54, end=78)])

    def test_parse_13(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('collector=CR 910025, E. E. Makela ;'),
            [])

    def test_parse_14(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(
                'Embryos of AF 48621. Eight embryos of AF 48621.  CR=6'),
            [NumericTrait(
                value=6, units=None, units_inferred=True, start=49, end=53)])

    def test_parse_15(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('snap 47: middle Cow Cr.'),
            [])

    def test_parse_16(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('headwaters Kaluich Cr, ca 1500 ft'),
            [])

    def test_parse_17(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(
                'sex=female ; total length=158 mm; tail length=28 mm; '
                'hind foot with claw=20 mm; ear from notch=12 mm; '
                'weight=60 g; reproductive data=embryos 2R,3L CR=15mm '
                'left intact'),
            [NumericTrait(
                value=15, units='mm', units_inferred=False,
                start=147, end=154)])
