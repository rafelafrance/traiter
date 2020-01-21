# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from traiter_vertnet.trait import Trait
from traiter_vertnet.parsers.embryo_count import EMBRYO_COUNT


class TestEmbryoCount(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('pregnant; 4 emb'),
            [Trait(value=4, start=10, end=15)])

    def test_parse_02(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('not pregnant; no embs'),
            [Trait(value=0, start=14, end=21)])

    def test_parse_03(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('pregnant; 4 emb 3L 1R'),
            [Trait(value=4, left=3, right=1, start=10, end=21)])

    def test_parse_04(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('embryos 2R-1L'),
            [Trait(value=3, left=1, right=2, start=0, end=13)])

    def test_parse_05(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('embryo of 34402'),
            [])

    def test_parse_06(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('138-62-18-6  12.4g  scars  emb.1R,1L; '),
            [Trait(value=2, left=1, right=1, start=27, end=36)])

    def test_parse_07(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                '; reproductive data=embryos: 4 right , 2 left  ;'),
            [Trait(value=6, left=2, right=4, start=20, end=45)])

    def test_parse_08(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                '; reproductive data=embryos: 4 right , 2 left  ;'),
            [Trait(value=6, left=2, right=4, start=20, end=45)])

    def test_parse_09(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('7 embryos, 4 male, and 3 female'),
            [Trait(value=7, male=4, female=3, start=0, end=31)])

    def test_parse_10(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('reproductive data=5 embryos (3L, 2R);'),
            [Trait(value=5, left=3, right=2, start=18, end=35)])

    def test_parse_11(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                'reproductive data=Vagina open.  4 small embryos.'),
            [Trait(value=4, start=32, end=47)])

    def test_parse_12(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('; 4 emb. x 07 mm, 3L2R", "weight":"23.0"'),
            [Trait(value=4, left=3, right=2, start=2, end=22)])

    def test_parse_13(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('; 3 emb. x 06 mm.",'),
            [Trait(value=3, start=2, end=7)])

    def test_parse_14(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('reproductive data: 3 embryos - 14 mm, 2R/1L;'),
            [Trait(value=3, left=1, right=2, start=19, end=43)])

    def test_parse_15(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Med. nipples, no scars or embryos, mod. fat'),
            [Trait(value=0, start=14, end=33)])

    def test_parse_16(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Fetus of AF 25577 (SHEID-99).'),
            [])

    def test_parse_17(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(', 4 fetuses on left, 1 on right'),
            [Trait(value=5, left=4, right=1, start=2, end=31)])

    def test_parse_18(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('This specimen contained 4 fetuses'),
            [Trait(value=4, start=24, end=33)])

    def test_parse_19(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('; age class=fetus'),
            [])

    def test_parse_20(self):
        self.assertEqual(
            EMBRYO_COUNT.parse("ONLY. 3 VERY LARGE FOETI(50).  REC'D FROM."),
            [Trait(value=3, start=6, end=24)])

    def test_parse_21(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                "'Foeti: 2R4L=6'; Donator: Dartmouth College Museum."),
            [Trait(value=6, left=4, right=2, start=1, end=12)])

    def test_parse_22(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('Fetus; Cruise #9999; Fetus of LACM 91773'),
            [])

    def test_parse_23(self):
        self.assertEqual(
            EMBRYO_COUNT.parse(
                '; reproductive data=7 near term embryos 95L, 2R)'),
            [Trait(value=97, left=95, right=2, start=32, end=47)])

    def test_parse_24(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('embryos of NK 125721, embryos NK 125726A-D'),
            [])

    def test_parse_25(self):
        self.assertEqual(
            EMBRYO_COUNT.parse('embryos of NK 125721, embryos NK 125726A-D'),
            [])
