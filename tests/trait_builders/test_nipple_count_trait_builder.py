import unittest
from pylib.numeric_trait import NumericTrait
from pylib.trait_builders.nipple_count_trait_builder \
    import NippleCountTraitBuilder


class TestNippleCountTraitBuilder(unittest.TestCase):

    parser = NippleCountTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            self.parser.parse('6 mammae, nipples prominent, ovaries 5 mm'),
            [NumericTrait(value=6, start=0, end=8)])

    def test_parse_02(self):
        self.assertEqual(
            self.parser.parse('1:2 = 6 mammae'),
            [NumericTrait(value=6, notation='1:2 = 6', start=0, end=14)])

    def test_parse_03(self):
        self.assertEqual(
            self.parser.parse('6 inguinal mammae visible but small;'),
            [NumericTrait(value=6, start=0, end=17)])

    def test_parse_04(self):
        self.assertEqual(
            self.parser.parse('mammae 2+2'),
            [])

    def test_parse_05(self):
        self.assertEqual(
            self.parser.parse('0 : 2 = 4 mammae'),
            [NumericTrait(value=4, notation='0 : 2 = 4', start=0, end=16)])

    def test_parse_06(self):
        self.assertEqual(
            self.parser.parse('mammae: 1 + 2 = 6'),
            [NumericTrait(value=6, notation='1 + 2 = 6', start=0, end=17)])

    def test_parse_07(self):
        self.assertEqual(
            self.parser.parse('3 pec, 3 ing mammae'),
            [NumericTrait(value=6, notation='3 pec, 3 ing', start=0, end=19)])

    def test_parse_08(self):
        self.assertEqual(
            self.parser.parse('(mammae: 1 pr + 2 pr = 6)'),
            [NumericTrait(
                value=6, notation='1 pr + 2 pr = 6', start=1, end=24)])

    def test_parse_09(self):
        self.assertEqual(
            self.parser.parse('4 teats exposed, mammary glands developed,'),
            [NumericTrait(value=4, start=0, end=7)])

    def test_parse_10(self):
        self.assertEqual(
            self.parser.parse('6 conspicuous mammae;'),
            [NumericTrait(value=6, start=0, end=20)])

    def test_parse_11(self):
        self.assertEqual(
            self.parser.parse('98 mammalian jaws and jaw fragments,'),
            [])

    def test_parse_12(self):
        self.assertEqual(
            self.parser.parse('; CR-9; mammary tissue present;'),
            [])

    def test_parse_13(self):
        self.assertEqual(
            self.parser.parse('a fauna of about 800 mammal teeth'),
            [])

    def test_parse_14(self):
        self.assertEqual(
            self.parser.parse('MISC. # IS 70034, NIPPLES ENLARGED'),
            [])

    def test_parse_15(self):
        self.assertEqual(
            self.parser.parse(
                'Source: MRS. ID# 42-1111.  Mammary development,'),
            [])

    def test_parse_16(self):
        self.assertEqual(
            self.parser.parse('CR:14 LG TEATS 98% LEAF,2%'),
            [])
