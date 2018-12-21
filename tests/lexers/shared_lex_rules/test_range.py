# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.lex_base import LexBase
import lib.lexers.shared_lex_rules as rule


LEX = LexBase()
LEX.lex_rules = [rule.range, rule.number, rule.word, rule.sep]


class TestRange(unittest.TestCase):

    def compare_tokens(self, text, expect):
        tokens = LEX.tokenize(text)
        actual = [(t.token, text[t.start:t.end]) for t in tokens]
        self.assertEqual(actual, expect)

    def test_range_01(self):
        text = '12345.6'
        expect = [('range', '12345.6')]
        self.compare_tokens(text, expect)

    def test_range_02(self):
        text = '12-34'
        expect = [('range', '12-34')]
        self.compare_tokens(text, expect)

    def test_range_03(self):
        text = '1984-10-22'
        expect = [('number', '1984'), ('number', '10'), ('number', '22')]
        self.compare_tokens(text, expect)

    def test_range_04(self):
        text = '12-34 to'
        expect = [('number', '12'), ('number', '34'), ('word', 'to')]
        self.compare_tokens(text, expect)

    def test_range_05(self):
        text = 'before 12 to 34 after'
        expect = [('word', 'before'), ('range', '12 to 34'), ('word', 'after')]
        self.compare_tokens(text, expect)

    def test_range_06(self):
        text = 'before 12 to 34 to 56 after'
        expect = [('word', 'before'),
                  ('number', '12'),
                  ('word', 'to'),
                  ('number', '34'),
                  ('word', 'to'),
                  ('number', '56'),
                  ('word', 'after')]
        self.compare_tokens(text, expect)

    def test_range_07(self):
        text = 'before 12 to 34 and 56 after'
        expect = [('word', 'before'),
                  ('range', '12 to 34'),
                  ('word', 'and'),
                  ('range', '56'),
                  ('word', 'after')]
        self.compare_tokens(text, expect)
