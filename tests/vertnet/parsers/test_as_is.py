# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from traiter_vertnet.trait import Trait
from traiter_vertnet.parsers.as_is import AS_IS


class TestAsIs(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            AS_IS.parse('word'),
            [Trait(value='word', as_is=True, start=0, end=4)])

    def test_parse_02(self):
        self.assertEqual(
            AS_IS.parse(' word  '),
            [Trait(value='word', as_is=True, start=1, end=5)])

    def test_parse_03(self):
        self.assertEqual(
            AS_IS.parse(' x  '),
            [Trait(value='x', as_is=True, start=1, end=2)])

    def test_parse_04(self):
        self.assertEqual(
            AS_IS.parse('x'),
            [Trait(value='x', as_is=True, start=0, end=1)])

    def test_parse_05(self):
        self.assertEqual(AS_IS.parse(''), [])

    def test_parse_06(self):
        self.assertEqual(AS_IS.parse('  '), [])

    def test_parse_07(self):
        self.assertEqual(
            AS_IS.parse(' word  word '),
            [Trait(value='word  word', as_is=True, start=1, end=11)])
