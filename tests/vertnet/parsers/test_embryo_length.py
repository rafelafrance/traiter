# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.embryo_length import EMBRYO_LENGTH


class TestEmbryoLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('crown-rump length=13 mm'),
            [Trait(
                value=13, units='mm', units_inferred=False, start=0, end=23)])

    def test_parse_02(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('Embryo crown-rump length 22'),
            [Trait(
                value=22, units=None, units_inferred=True, start=0, end=27)])

    def test_parse_03(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(
                'reproductive data: 4 embryos - 15 mm, crown-rump length'),
            [Trait(
                value=15, units='mm', units_inferred=False, start=21, end=48)])

    def test_parse_04(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(', CR (crown-rump length) =7 ;'),
            [Trait(
                value=7, units=None, units_inferred=True, start=6, end=27)])

    def test_parse_05(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(', CRL=59 mm; '),
            [Trait(
                value=59, units='mm', units_inferred=False, start=2, end=11)])

    def test_parse_06(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('pregnant; 1 emb; cr-28'),
            [Trait(
                value=28, units=None, units_inferred=True, start=17, end=22)])

    def test_parse_07(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('embryos left horn, cr-rump: 23mm.'),
            [Trait(
                value=23, units='mm', units_inferred=False, start=19, end=32)])

    def test_parse_08(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('4 embs/1R/3L/cr=2mm'),
            [Trait(
                value=2, units='mm', units_inferred=False, start=13, end=19)])

    def test_parse_09(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('3 embs/2L+2R/cr=X34mm'),
            [Trait(
                value=34, units='mm', units_inferred=False, start=13, end=21)])

    def test_parse_10(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(', cr=5x5 ;'),
            [Trait(
                value=[5, 5], units=None, units_inferred=True,
                start=2, end=8)])

    def test_parse_11(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(
                'sex=recorded as unknown ; reproductive data=cr=9x8mm'),
            [Trait(
                value=[9, 8], units='mm', units_inferred=False,
                start=44, end=52)])

    def test_parse_12(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(
                'reproductive data=Embryos: 2 (1 resorbing) R, 3 Left, '
                'crown-rump length, 36 mm.'),
            [Trait(
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
            [Trait(
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
            [Trait(
                value=15, units='mm', units_inferred=False,
                start=147, end=154)])

    def test_parse_18(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('OCGR pg, 4 embs, 2R, 2L, 12 mm 4 2 2'),
            [
                Trait(
                    value=12, units='mm', units_inferred=False,
                    start=11, end=36),
                Trait(
                    value=4, units='mm', units_inferred=True,
                    start=11, end=36),
                Trait(
                    value=2, units='mm', units_inferred=True,
                    start=11, end=36),
                Trait(
                    value=2, units='mm', units_inferred=True,
                    start=11, end=36)])

    def test_parse_19(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('Mammals 7 embs, 3 mm'),
            [Trait(
                value=3, units='mm', units_inferred=False,
                start=10, end=20)])

    def test_parse_20(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('Mammals 3 embs, 24mm'),
            [Trait(
                value=24, units='mm', units_inferred=False,
                start=10, end=20)])

    def test_parse_21(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('3 embs, 2L, 1R, 19 mm, 17 mm, 17 mm'),
            [
                Trait(
                    value=19, units='mm', units_inferred=False,
                    start=2, end=35),
                Trait(
                    value=17, units='mm', units_inferred=False,
                    start=2, end=35),
                Trait(
                    value=17, units='mm', units_inferred=False,
                    start=2, end=35)])

    def test_parse_22(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse(
                'Mammals vagina open; mammae tiny; not lactating9 embryos; '
                'cr-10 ?'),
            [Trait(
                value=10, units=None, units_inferred=True,
                start=58, end=65, uncertain=True)])

    def test_parse_23(self):
        self.assertEqual(
            EMBRYO_LENGTH.parse('4 embs: 2(R)&2(L)=9mm '),
            [Trait(
                value=9, units='mm', units_inferred=False,
                start=2, end=21)])
