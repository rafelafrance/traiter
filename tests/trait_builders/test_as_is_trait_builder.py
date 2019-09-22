import unittest
from pylib.trait import Trait
from pylib.trait_builders.as_is_trait_builder import AsIsTraitBuilder


class TestAsIsTraitBuilder(unittest.TestCase):

    parser = AsIsTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            self.parser.parse('word'),
            [Trait(value='word', as_is=True, start=0, end=4)])

    def test_parse_02(self):
        self.assertEqual(
            self.parser.parse(' word  '),
            [Trait(value='word', as_is=True, start=1, end=5)])

    def test_parse_03(self):
        self.assertEqual(
            self.parser.parse(' x  '),
            [Trait(value='x', as_is=True, start=1, end=2)])

    def test_parse_04(self):
        self.assertEqual(
            self.parser.parse('x'),
            [Trait(value='x', as_is=True, start=0, end=1)])

    def test_parse_05(self):
        self.assertEqual(self.parser.parse(''), [])

    def test_parse_06(self):
        self.assertEqual(self.parser.parse('  '), [])

    def test_parse_07(self):
        self.assertEqual(
            self.parser.parse(' word  word '),
            [Trait(value='word  word', as_is=True, start=1, end=11)])
