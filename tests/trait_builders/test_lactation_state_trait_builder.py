import unittest
from pylib.trait import Trait
from pylib.trait_builders.lactation_state_trait_builder \
    import LactationStateTraitBuilder


PAR = None


class TestSexTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = LactationStateTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('lactating'),
            [Trait(value='lactating', start=0, end=9)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('not pregnant; not lactating'),
            [Trait(value='not lactating', start=14, end=27)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('No embs; post lact.'),
            [Trait(value='post lact', start=9, end=18)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('non-lactating'),
            [Trait(value='non-lactating', start=0, end=13)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('lactating?'),
            [Trait(value='lactating?', start=0, end=10)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('recently lactating'),
            [Trait(value='recently lactating', start=0, end=18)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('small mammaries, no lactation,'),
            [Trait(value='no lactation', start=17, end=29)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('just finished lactating'),
            [Trait(value='just finished lactating', start=0, end=23)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('reproductive data=non-lactating, non-pregnant'),
            [Trait(value='non-lactating', start=18, end=31)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('Tail pencil; Not nursing, no embryos;'),
            [Trait(value='not nursing', start=13, end=24)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('no. 8552; suckling'),
            [Trait(value='suckling', start=10, end=18)])
