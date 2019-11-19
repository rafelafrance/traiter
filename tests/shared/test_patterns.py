import unittest
from pylib.stacked_regex.parser import Parser
from pylib.stacked_regex.token import Token
from pylib.shared.patterns import RULE


class TestSharedPatterns(unittest.TestCase):

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
        parser = Parser(RULE['range_set'])
        actual = parser.parse('12 to 34')
        expect = [Token(
            rule=RULE['range'], span=(0, 8),
            groups={'number': ['12', '34'], 'to': 'to',
                    'range': '12 to 34'})]
        self.assertEqual(actual, expect)

    def test_range_02(self):
        parser = Parser(RULE['range_set'])
        actual = parser.parse('12.3-45.6')
        expect = [Token(
            rule=RULE['range'], span=(0, 9),
            groups={'number': ['12.3', '45.6'], 'dash': '-',
                    'range': '12.3-45.6'})]
        self.assertEqual(actual, expect)

    def test_range_03(self):
        parser = Parser(RULE['range_set'])
        actual = parser.parse('9 12.3 - 45.6 8')
        expect = [
            Token(RULE['number'], span=(0, 1), groups={'number': '9'}),
            Token(
                rule=RULE['range'], span=(2, 13),
                groups={'number': ['12.3', '45.6'], 'range': '12.3 - 45.6',
                        'dash': '-'}),
            Token(RULE['number'], span=(14, 15), groups={'number': '8'})]
        self.assertEqual(actual, expect)

    def test_range_04(self):
        parser = Parser(RULE['range_set'])
        actual = parser.parse('12-34-56')
        expect = [
            Token(rule=RULE['number'], span=(0, 2), groups={'number': '12'}),
            Token(rule=RULE['dash'], span=(2, 3), groups={'dash': '-'}),
            Token(rule=RULE['number'], span=(3, 5), groups={'number': '34'}),
            Token(rule=RULE['dash'], span=(5, 6), groups={'dash': '-'}),
            Token(rule=RULE['number'], span=(6, 8), groups={'number': '56'})]
        self.assertEqual(actual, expect)

    def test_cross_01(self):
        parser = Parser(RULE['cross_set'])
        actual = parser.parse('12x34')
        expect = [Token(
            rule=RULE['cross'], span=(0, 5),
            groups={'number': ['12', '34'], 'x': 'x',
                    'cross': '12x34'})]
        self.assertEqual(actual, expect)

    def test_cross_02(self):
        parser = Parser(RULE['cross_set'])
        actual = parser.parse('12.3 by 45.6')
        expect = [Token(
            rule=RULE['cross'], span=(0, 12),
            groups={'number': ['12.3', '45.6'], 'by': 'by',
                    'cross': '12.3 by 45.6'})]
        self.assertEqual(actual, expect)

    def test_cross_03(self):
        self.maxDiff = None
        parser = Parser(RULE['cross_set'])
        actual = parser.parse('9 12.3 x 45.6 8')
        expect = [
            Token(RULE['number'], span=(0, 1), groups={'number': '9'}),
            Token(
                rule=RULE['cross'], span=(2, 13),
                groups={'number': ['12.3', '45.6'], 'x': 'x',
                        'cross': '12.3 x 45.6'}),
            Token(RULE['number'], span=(14, 15), groups={'number': '8'})]
        self.assertEqual(actual, expect)

    def test_cross_04(self):
        parser = Parser(RULE['cross_set'])
        actual = parser.parse('12x34x56')
        expect = [
            Token(
                rule=RULE['cross'], span=(0, 5),
                groups={'number': ['12', '34'], 'x': 'x',
                        'cross': '12x34'}),
            Token(rule=RULE['x'], span=(5, 6), groups={'x': 'x'}),
            Token(rule=RULE['number'], span=(6, 8), groups={'number': '56'})]
        self.assertEqual(actual, expect)

    def test_cross_05(self):
        parser = Parser(RULE['cross_set'])
        actual = parser.parse('3x1.5mm')
        expect = [Token(
            rule=RULE['cross'], span=(0, 5),
            groups={'number': ['3', '1.5'], 'x': 'x',
                    'cross': '3x1.5'})]
        self.assertEqual(actual, expect)

    def test_fraction_01(self):
        parser = Parser(RULE['fraction_set'])
        actual = parser.parse('12/34')
        expect = [Token(
            rule=RULE['fraction'], span=(0, 5),
            groups={'number': ['12', '34'], 'slash': '/',
                    'fraction': '12/34'})]
        self.assertEqual(actual, expect)

    def test_fraction_02(self):
        parser = Parser(RULE['fraction_set'])
        actual = parser.parse('12/34/56')
        expect = [
            Token(rule=RULE['number'], span=(0, 2),
                  groups={'number': '12'}),
            Token(rule=RULE['slash'], span=(2, 3), groups={'slash': '/'}),
            Token(rule=RULE['number'], span=(3, 5),
                  groups={'number': '34'}),
            Token(rule=RULE['slash'], span=(5, 6), groups={'slash': '/'}),
            Token(rule=RULE['number'], span=(6, 8),
                  groups={'number': '56'})]
        self.assertEqual(actual, expect)

    def test_uuid_01(self):
        parser = Parser(RULE['uuid'])
        actual = parser.parse('ddf2d94a-0a49-11ea-a133-000000000004')
        expect = [Token(
            RULE['uuid'], span=(0, 36),
            groups={'uuid': 'ddf2d94a-0a49-11ea-a133-000000000004'})]
        self.assertEqual(actual, expect)
