import unittest
from pylib.stacked_regex.parser import Parser
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import producer
from pylib.shared.patterns import RULE


def nop(token):
    """Create a dummy function for tests."""
    return token


class TestSharedPatterns(unittest.TestCase):

    range_product = producer(nop, 'range', 'range_product')
    cross_product = producer(nop, 'cross', 'cross_product')
    fraction_product = producer(nop, 'fraction', 'fraction_product')

    def test_number_01(self):
        parser = Parser(rules=[RULE['number']])
        actual = parser.parse('123')
        expect = [Token(
            RULE['number'], span=(0, 3), groups={'number': '123'})]
        self.assertEqual(actual, expect)

    def test_number_02(self):
        parser = Parser(rules=[RULE['number']])
        actual = parser.parse('12.3')
        expect = [Token(
            RULE['number'], span=(0, 4), groups={'number': '12.3'})]
        self.assertEqual(actual, expect)

    def test_number_03(self):
        parser = Parser(rules=[RULE['number']])
        actual = parser.parse('   12.3 x')
        expect = [Token(
            RULE['number'], span=(3, 7), groups={'number': '12.3'})]
        self.assertEqual(actual, expect)

    def test_number_04(self):
        parser = Parser(rules=[RULE['number']])
        actual = parser.parse('12.3 4')
        expect = [
            Token(RULE['number'], span=(0, 4), groups={'number': '12.3'}),
            Token(RULE['number'], span=(5, 6), groups={'number': '4'})]
        self.assertEqual(actual, expect)

    def test_range_01(self):
        parser = Parser([RULE['range_set'], self.range_product])
        actual = parser.parse('12 to 34')
        expect = [Token(
            rule=self.range_product, span=(0, 8),
            groups={'number': ['12', '34'], 'to': 'to',
                    'range': '12 to 34',
                    'range_product': '12 to 34'})]
        self.assertEqual(actual, expect)

    def test_range_02(self):
        parser = Parser([RULE['range_set'], self.range_product])
        actual = parser.parse('12.3-45.6')
        expect = [Token(
            rule=self.range_product, span=(0, 9),
            groups={'number': ['12.3', '45.6'], 'dash': '-',
                    'range': '12.3-45.6',
                    'range_product': '12.3-45.6'})]
        self.assertEqual(actual, expect)

    def test_range_03(self):
        parser = Parser([RULE['range_set'], self.range_product])
        actual = parser.parse('9 12.3 - 45.6 8')
        expect = [
            Token(
                rule=self.range_product, span=(2, 13),
                groups={'number': ['12.3', '45.6'], 'dash': '-',
                        'range': '12.3 - 45.6',
                        'range_product': '12.3 - 45.6'})]
        self.assertEqual(actual, expect)

    def test_range_04(self):
        parser = Parser([RULE['range_set'], self.range_product])
        actual = parser.parse('12-34-56')
        expect = []
        self.assertEqual(actual, expect)

    def test_range_05(self):
        parser = Parser([RULE['range_set'], self.range_product])
        actual = parser.parse('12.3mm - 45.6mm')
        expect = [
            Token(
                rule=self.range_product, span=(0, 15),
                groups={'number': ['12.3', '45.6'],
                        'range': '12.3mm - 45.6mm',
                        'range_product': '12.3mm - 45.6mm',
                        'metric_len': ['mm', 'mm'], 'len_units': ['mm', 'mm'],
                        'units': ['mm', 'mm'], 'dash': '-'})]
        self.assertEqual(actual, expect)

    def test_range_06(self):
        parser = Parser([RULE['range_set'], self.range_product])
        actual = parser.parse('12.3 - 45.6mm')
        expect = [
            Token(
                rule=self.range_product, span=(0, 13),
                groups={'number': ['12.3', '45.6'],
                        'range_product': '12.3 - 45.6mm',
                        'range': '12.3 - 45.6mm',
                        'metric_len': 'mm', 'len_units': 'mm', 'units': 'mm',
                        'dash': '-'})]
        self.assertEqual(actual, expect)

    def test_range_07(self):
        parser = Parser([RULE['range_set'], self.range_product])
        actual = parser.parse('12.3mm')
        expect = [
            Token(
                rule=self.range_product, span=(0, 6),
                groups={'number': '12.3',
                        'range_product': '12.3mm',
                        'range': '12.3mm',
                        'metric_len': 'mm', 'len_units': 'mm', 'units': 'mm'})]
        self.assertEqual(actual, expect)

    def test_cross_01(self):
        parser = Parser([RULE['cross_set'], self.cross_product])
        actual = parser.parse('12x34')
        expect = [Token(
            rule=self.cross_product, span=(0, 5),
            groups={'number': ['12', '34'], 'x': 'x',
                    'cross': '12x34', 'cross_product': '12x34'})]
        self.assertEqual(actual, expect)

    def test_cross_02(self):
        parser = Parser([RULE['cross_set'], self.cross_product])
        actual = parser.parse('12.3 by 45.6')
        expect = [Token(
            rule=self.cross_product, span=(0, 12),
            groups={'number': ['12.3', '45.6'], 'by': 'by',
                    'cross': '12.3 by 45.6', 'cross_product': '12.3 by 45.6'})]
        self.assertEqual(actual, expect)

    def test_cross_03(self):
        parser = Parser([RULE['cross_set'], self.cross_product])
        actual = parser.parse('9 12.3 x 45.6 8')
        expect = [
            Token(
                rule=self.cross_product, span=(2, 13),
                groups={'number': ['12.3', '45.6'], 'x': 'x',
                        'cross': '12.3 x 45.6',
                        'cross_product': '12.3 x 45.6'})]
        self.assertEqual(actual, expect)

    def test_cross_04(self):
        parser = Parser([RULE['cross_set'], self.cross_product])
        actual = parser.parse('12x34x56')
        expect = [
            Token(
                rule=self.cross_product, span=(0, 5),
                groups={'number': ['12', '34'], 'x': 'x',
                        'cross': '12x34', 'cross_product': '12x34'})]
        self.assertEqual(actual, expect)

    def test_cross_05(self):
        parser = Parser([RULE['cross_set'], self.cross_product])
        actual = parser.parse('3x1.5mm')
        expect = [Token(
            rule=self.cross_product, span=(0, 7),
            groups={'number': ['3', '1.5'], 'x': 'x',
                    'cross': '3x1.5mm', 'cross_product': '3x1.5mm',
                    'metric_len': 'mm', 'len_units': 'mm'})]
        self.assertEqual(actual, expect)

    def test_cross_06(self):
        parser = Parser([RULE['cross_set'], self.cross_product])
        actual = parser.parse('3mmx1.5mm')
        expect = [Token(
            rule=self.cross_product, span=(0, 9),
            groups={'number': ['3', '1.5'], 'x': 'x',
                    'cross': '3mmx1.5mm', 'cross_product': '3mmx1.5mm',
                    'metric_len': ['mm', 'mm'], 'len_units': ['mm', 'mm']})]
        self.assertEqual(actual, expect)

    def test_cross_07(self):
        parser = Parser([RULE['cross_set'], self.cross_product])
        actual = parser.parse('12.3mm')
        expect = [
            Token(
                rule=self.cross_product, span=(0, 6),
                groups={'number': '12.3',
                        'cross': '12.3mm', 'cross_product': '12.3mm',
                        'metric_len': 'mm', 'len_units': 'mm'})]
        self.assertEqual(actual, expect)

    def test_fraction_01(self):
        parser = Parser([RULE['fraction_set'], self.fraction_product])
        actual = parser.parse('12/34')
        expect = [Token(
            rule=self.fraction_product, span=(0, 5),
            groups={'number': ['12', '34'], 'slash': '/',
                    'fraction': '12/34', 'fraction_product': '12/34'})]
        self.assertEqual(actual, expect)

    def test_fraction_02(self):
        parser = Parser([RULE['fraction_set'], self.fraction_product])
        actual = parser.parse('12/34/56')
        expect = []
        self.assertEqual(actual, expect)

    def test_uuid_01(self):
        parser = Parser(RULE['uuid'])
        actual = parser.parse('ddf2d94a-0a49-11ea-a133-000000000004')
        expect = [Token(
            RULE['uuid'], span=(0, 36),
            groups={'uuid': 'ddf2d94a-0a49-11ea-a133-000000000004'})]
        self.assertEqual(actual, expect)
