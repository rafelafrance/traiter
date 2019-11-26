# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.nipple_count import NIPPLE_COUNT


class TestNippleCount(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('6 mammae, nipples prominent, ovaries 5 mm'),
            [Trait(value=6, start=0, end=8)])

    def test_parse_02(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('1:2 = 6 mammae'),
            [Trait(value=6, notation='1:2 = 6', start=0, end=14)])

    def test_parse_03(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('6 inguinal mammae visible but small;'),
            [Trait(value=6, start=0, end=17)])

    def test_parse_04(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('mammae 2+2'),
            [])

    def test_parse_05(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('0 : 2 = 4 mammae'),
            [Trait(value=4, notation='0 : 2 = 4', start=0, end=16)])

    def test_parse_06(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('mammae: 1 + 2 = 6'),
            [Trait(value=6, notation='1 + 2 = 6', start=0, end=17)])

    def test_parse_07(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('3 pec, 3 ing mammae'),
            [Trait(value=6, notation='3 pec, 3 ing', start=0, end=19)])

    def test_parse_08(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('(mammae: 1 pr + 2 pr = 6)'),
            [Trait(
                value=6, notation='1 pr + 2 pr = 6', start=1, end=24)])

    def test_parse_09(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('4 teats exposed, mammary glands developed,'),
            [Trait(value=4, start=0, end=7)])

    def test_parse_10(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('6 conspicuous mammae;'),
            [Trait(value=6, start=0, end=20)])

    def test_parse_11(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('98 mammalian jaws and jaw fragments,'),
            [])

    def test_parse_12(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('; CR-9; mammary tissue present;'),
            [])

    def test_parse_13(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('a fauna of about 800 mammal teeth'),
            [])

    def test_parse_14(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('MISC. # IS 70034, NIPPLES ENLARGED'),
            [])

    def test_parse_15(self):
        self.assertEqual(
            NIPPLE_COUNT.parse(
                'Source: MRS. ID# 42-1111.  Mammary development,'),
            [])

    def test_parse_16(self):
        self.assertEqual(
            NIPPLE_COUNT.parse('CR:14 LG TEATS 98% LEAF,2%'),
            [])
