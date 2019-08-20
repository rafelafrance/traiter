import unittest
from lib.numeric_trait import NumericTrait
from lib.trait_builders.nipple_count_trait_builder \
    import NippleCountTraitBuilder


PAR = None


class TestNippleCountTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = NippleCountTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('6 mammae, nipples prominent, ovaries 5 mm'),
            [NumericTrait(value=6, start=0, end=8)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('1:2 = 6 mammae'),
            [NumericTrait(value=6, notation='1:2 = 6', start=0, end=14)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('6 inguinal mammae visible but small;'),
            [NumericTrait(value=6, start=0, end=17)])

    # def test_parse_04(self):
    #     self.assertEqual(
    #         PAR.parse('mammae 2+2'),
    #         [])
