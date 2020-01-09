"""Test shared patterns for plant parsers."""

import unittest
from pylib.stacked_regex.parser import Parser
from pylib.stacked_regex.token import Token
from pylib.efloras.shared_patterns import VOCAB


def nop(token):
    """Create a dummy function for tests."""
    return token


class TestSharedPatterns(unittest.TestCase):
    """Test shared patterns for plant parsers."""

    number_product = VOCAB.producer(
        nop, 'number', capture=False, name='number_product')
    range_product = VOCAB.producer(
        nop, 'range', capture=False, name='range_product')
    cross_product = VOCAB.producer(
        nop, 'cross', capture=False, name='cross_product')
    upper_product = VOCAB.producer(
        nop, 'cross_upper', capture=False, name='upper_product')

    number_parser = Parser(number_product)
    range_parser = Parser(range_product)
    cross_parser = Parser(cross_product)
    upper_parser = Parser(upper_product)

    def test_number_01(self):
        """It handles integers."""
        actual = self.number_parser.parse('123')
        expect = [Token(
            VOCAB['number_product'], span=(0, 3), groups={'number': '123'})]
        self.assertEqual(actual, expect)

    def test_number_02(self):
        """It handles decimal points."""
        actual = self.number_parser.parse('12.3')
        expect = [Token(
            VOCAB['number_product'], span=(0, 4), groups={'number': '12.3'})]
        self.assertEqual(actual, expect)

    def test_number_03(self):
        """It parses a partial cross."""
        actual = self.number_parser.parse('   12.3 x')
        expect = [Token(
            VOCAB['number_product'], span=(3, 7), groups={'number': '12.3'})]
        self.assertEqual(actual, expect)

    def test_number_04(self):
        """It keeps numbers separate."""
        actual = self.number_parser.parse('12.3 4')
        expect = [
            Token(VOCAB['number_product'], span=(0, 4),
                  groups={'number': '12.3'}),
            Token(VOCAB['number_product'], span=(5, 6),
                  groups={'number': '4'})]
        self.assertEqual(actual, expect)

    def test_range_01(self):
        """It interprets a single number as the high end of a range."""
        actual = self.range_parser.parse('123')
        expect = [Token(
            VOCAB['range_product'], span=(0, 3),
            groups={'number': '123', 'low': '123'})]
        self.assertEqual(actual, expect)

    def test_range_02(self):
        """It parses a simple range."""
        actual = self.range_parser.parse('123-45')
        expect = [Token(
            VOCAB['range_product'], span=(0, 6),
            groups={'number': ['123', '45'], 'low': '123', 'high': '45'})]
        self.assertEqual(actual, expect)

    def test_range_03(self):
        """It parses the all numbers of a range."""
        actual = self.range_parser.parse('(12-)23-34(-45)')
        expect = [Token(
            VOCAB['range_product'], span=(0, 15),
            groups={
                'number': ['12', '23', '34', '45'],
                'low': '23', 'high': '34',
                'min': '12', 'max': '45'})]
        self.assertEqual(actual, expect)

    def test_range_04(self):
        """It handles a missing minimum."""
        actual = self.range_parser.parse('23-34(-45)')
        expect = [Token(
            VOCAB['range_product'], span=(0, 10),
            groups={
                'number': ['23', '34', '45'],
                'low': '23', 'high': '34', 'max': '45'})]
        self.assertEqual(actual, expect)

    def test_range_05(self):
        """It handles a missing maximum."""
        actual = self.range_parser.parse('(12-)23-34')
        expect = [Token(
            VOCAB['range_product'], span=(0, 10),
            groups={
                'number': ['12', '23', '34'],
                'low': '23', 'high': '34', 'min': '12'})]
        self.assertEqual(actual, expect)

    def test_range_06(self):
        """It does not pick up units in a range."""
        actual = self.range_parser.parse('blade 1.5–5(–7) cm')
        expect = [Token(
            VOCAB['range_product'], span=(6, 15),
            groups={
                'number': ['1.5', '5', '7'],
                'low': '1.5', 'high': '5', 'max': '7'})]
        self.assertEqual(actual, expect)

    def test_cross_01(self):
        """It handles a range as a cross."""
        actual = self.cross_parser.parse('(12-)23-34')
        expect = [Token(
            VOCAB['cross_product'], span=(0, 10),
            groups={
                'number': ['12', '23', '34'],
                'min_length': '12', 'low_length': '23', 'high_length': '34'})]
        self.assertEqual(actual, expect)

    def test_cross_02(self):
        """It handles a full cross."""
        actual = self.cross_parser.parse('(12-)23-34 × 45-56')
        expect = [Token(
            VOCAB['cross_product'], span=(0, 18),
            groups={
                'number': ['12', '23', '34', '45', '56'],
                'min_length': '12', 'low_length': '23', 'high_length': '34',
                'low_width': '45', 'high_width': '56'})]
        self.assertEqual(actual, expect)

    def test_upper_only_01(self):
        """It handles an upper only cross notation."""
        actual = self.upper_parser.parse('to 10 cm')
        expect = [Token(
            VOCAB['upper_product'], span=(0, 8),
            groups={
                'number': '10', 'units': 'cm',
                'high_length': '10', 'units_length': 'cm'})]
        self.assertEqual(actual, expect)
