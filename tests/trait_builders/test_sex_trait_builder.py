import unittest
from pylib.trait import Trait
from pylib.trait_builders.sex_trait_builder import SexTraitBuilder


class TestSexTraitBuilder(unittest.TestCase):

    parser = SexTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            self.parser.parse('sex=female ?'),
            [Trait(value='female ?', start=0, end=12)])

    def test_parse_02(self):
        self.assertEqual(
            self.parser.parse('sex=unknown ; crown-rump length=8 mm'),
            [Trait(value='unknown', start=0, end=13)])

    def test_parse_03(self):
        self.assertEqual(
            self.parser.parse('sex=F crown rump length=8 mm'),
            [Trait(value='f', start=0, end=5)])

    def test_parse_04(self):
        self.assertEqual(
            self.parser.parse('words male female unknown more words'),
            [Trait(value='male', start=6, end=10),
             Trait(value='female', start=11, end=17)])

    def test_parse_05(self):
        self.assertEqual(
            self.parser.parse('words male female male more words'),
            [Trait(value='male', start=6, end=10),
             Trait(value='female', start=11, end=17),
             Trait(value='male', start=18, end=22)])

    def test_parse_06(self):
        self.assertEqual(
            self.parser.parse('Respective sex and msmt. in mm'),
            [])

    def test_parse_07(self):
        self.assertEqual(
            self.parser.parse('male or female'),
            [Trait(value='male', start=0, end=4),
             Trait(value='female', start=8, end=14)])

    def test_parse_08(self):
        self.assertEqual(
            self.parser.parse('sex=unknown length=8 mm'),
            [Trait(value='unknown', start=0, end=11)])

    def test_parse_09(self):
        self.assertEqual(
            self.parser.parse('sex=female?'),
            [Trait(value='female?', start=0, end=11)])

    def test_parse_10(self):
        self.assertEqual(
            self.parser.parse('sex=not recorded ;'),
            [Trait(value='not recorded', start=0, end=18)])

    def test_parse_11(self):
        self.assertEqual(
            self.parser.parse('sex=male ; sex=male ;'),
            [Trait(value='male', start=0, end=10),
             Trait(value='male', start=11, end=21)])
