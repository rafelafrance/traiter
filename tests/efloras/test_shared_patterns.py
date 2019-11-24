"""Test shared patterns for plant parsers."""

import unittest
from pylib.stacked_regex.parser import Parser, scan
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import producer
from pylib.efloras.shared_patterns import RULE


def nop(token):
    """Create a dummy function for tests."""
    return token


class TestSharedPatterns(unittest.TestCase):
    """Test shared patterns for plant parsers."""

    range_product = producer(nop, 'range', 'range_product', capture=False)
    cross_product = producer(nop, 'cross', 'cross_product', capture=False)
    upper_product = producer(
        nop, 'cross_upper', 'upper_product', capture=False)

    range_parser = Parser([RULE['range_set'], range_product])
    cross_parser = Parser([RULE['cross_set'], cross_product])
    upper_parser = Parser([RULE['cross_upper_set'], upper_product])

    def test_number_01(self):
        """It handles integers."""
        actual = scan([RULE['number']], '123')
        expect = [Token(
            RULE['number'], span=(0, 3), groups={'number': '123'})]
        self.assertEqual(actual, expect)

    def test_number_02(self):
        """It handles decimal points."""
        actual = scan([RULE['number']], '12.3')
        expect = [Token(
            RULE['number'], span=(0, 4), groups={'number': '12.3'})]
        self.assertEqual(actual, expect)

    def test_number_03(self):
        """It parses a partial cross."""
        actual = scan([RULE['number']], '   12.3 x')
        expect = [Token(
            RULE['number'], span=(3, 7), groups={'number': '12.3'})]
        self.assertEqual(actual, expect)

    def test_number_04(self):
        """It keeps numbers separate."""
        actual = scan([RULE['number']], '12.3 4')
        expect = [
            Token(RULE['number'], span=(0, 4), groups={'number': '12.3'}),
            Token(RULE['number'], span=(5, 6), groups={'number': '4'})]
        self.assertEqual(actual, expect)

    def test_range_01(self):
        """It interprets a single number as the high end of a range."""
        actual = self.range_parser.parse('123')
        expect = [Token(
            self.range_product, span=(0, 3),
            groups={'number': '123', 'low': '123'})]
        self.assertEqual(actual, expect)

    def test_range_02(self):
        actual = self.range_parser.parse('123-45')
        expect = [Token(
            self.range_product, span=(0, 6),
            groups={'number': ['123', '45'], 'low': '123', 'high': '45'})]
        self.assertEqual(actual, expect)

    def test_range_03(self):
        actual = self.range_parser.parse('(12-)23-34(-45)')
        expect = [Token(
            self.range_product, span=(0, 15),
            groups={
                'number': ['12', '23', '34', '45'],
                'low': '23', 'high': '34',
                'min': '12', 'max': '45'})]
        self.assertEqual(actual, expect)

    def test_range_04(self):
        actual = self.range_parser.parse('23-34(-45)')
        expect = [Token(
            self.range_product, span=(0, 10),
            groups={
                'number': ['23', '34', '45'],
                'low': '23', 'high': '34', 'max': '45'})]
        self.assertEqual(actual, expect)

    def test_range_05(self):
        actual = self.range_parser.parse('(12-)23-34')
        expect = [Token(
            self.range_product, span=(0, 10),
            groups={
                'number': ['12', '23', '34'],
                'low': '23', 'high': '34', 'min': '12'})]
        self.assertEqual(actual, expect)

    def test_range_06(self):
        actual = self.range_parser.parse('blade 1.5–5(–7) cm')
        expect = [Token(
            self.range_product, span=(6, 15),
            groups={
                'number': ['1.5', '5', '7'],
                'low': '1.5', 'high': '5', 'max': '7'})]
        self.assertEqual(actual, expect)

    def test_cross_01(self):
        actual = self.cross_parser.parse('(12-)23-34')
        expect = [Token(
            self.cross_product, span=(0, 10),
            groups={
                'number': ['12', '23', '34'],
                'min_length': '12', 'low_length': '23', 'high_length': '34'})]
        self.assertEqual(actual, expect)

    def test_cross_02(self):
        actual = self.cross_parser.parse('(12-)23-34 × 45-56')
        expect = [Token(
            self.cross_product, span=(0, 18),
            groups={
                'number': ['12', '23', '34', '45', '56'],
                'min_length': '12', 'low_length': '23', 'high_length': '34',
                'low_width': '45', 'high_width': '56'})]
        self.assertEqual(actual, expect)

    def test_upper_only_01(self):
        actual = self.upper_parser.parse('to 10 cm')
        expect = [Token(
            self.upper_product, span=(0, 8),
            groups={
                'number': '10', 'units': 'cm',
                'high_length': '10', 'units_length': 'cm'})]
        self.assertEqual(actual, expect)
