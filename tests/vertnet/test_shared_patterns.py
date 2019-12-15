# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods

import unittest
from pylib.stacked_regex.parser import Parser
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import producer
from pylib.vertnet.shared_patterns import CATALOG


def nop(token):
    """Create a dummy function for tests."""
    return token


class TestSharedPatterns(unittest.TestCase):
    cross_product = producer(nop, 'cross')
    fraction_product = producer(nop, 'fraction')

    def test_cross_03(self):
        parser = Parser([CATALOG['cross'], self.cross_product])
        actual = parser.parse('9 12.3 x 45.6 8')
        expect = [
            Token(
                rule=self.cross_product, span=(2, 13),
                groups={'number': ['12.3', '45.6']})]
        self.assertEqual(actual, expect)

    def test_cross_04(self):
        parser = Parser([CATALOG['cross'], self.cross_product])
        actual = parser.parse('12x34x56')
        expect = [
            Token(
                rule=self.cross_product, span=(0, 5),
                groups={'number': ['12', '34']})]
        self.assertEqual(actual, expect)

    def test_cross_05(self):
        parser = Parser([CATALOG['cross'], self.cross_product])
        actual = parser.parse('3x1.5mm')
        expect = [Token(
            rule=self.cross_product, span=(0, 7),
            groups={'number': ['3', '1.5'],
                    'metric_len': 'mm', 'len_units': 'mm'})]
        self.assertEqual(actual, expect)

    def test_cross_06(self):
        parser = Parser([CATALOG['cross'], self.cross_product])
        actual = parser.parse('3mmx1.5mm')
        expect = [Token(
            rule=self.cross_product, span=(0, 9),
            groups={
                'number': ['3', '1.5'],
                'metric_len': ['mm', 'mm'], 'len_units': ['mm', 'mm']})]
        self.assertEqual(actual, expect)

    def test_cross_07(self):
        parser = Parser([CATALOG['cross'], self.cross_product])
        actual = parser.parse('12.3mm')
        expect = [
            Token(
                rule=self.cross_product, span=(0, 6),
                groups={'number': '12.3',
                        'metric_len': 'mm', 'len_units': 'mm'})]
        self.assertEqual(actual, expect)

    def test_fraction_01(self):
        parser = Parser([CATALOG['fraction'], self.fraction_product])
        actual = parser.parse('12/34')
        expect = [Token(
            rule=self.fraction_product, span=(0, 5),
            groups={'number': ['12', '34'],
                    'numerator': '12', 'denominator': '34'})]
        self.assertEqual(actual, expect)

    def test_fraction_02(self):
        parser = Parser([CATALOG['fraction'], self.fraction_product])
        actual = parser.parse('12/34/56')
        expect = []
        self.assertEqual(actual, expect)

    def test_uuid_01(self):
        parser = Parser(CATALOG['uuid'])
        actual = parser.parse('ddf2d94a-0a49-11ea-a133-000000000004')
        expect = [Token(
            CATALOG['uuid'], span=(0, 36),
            groups={})]
        self.assertEqual(actual, expect)
