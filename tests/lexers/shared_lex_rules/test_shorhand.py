# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.lex_base import LexBase
import lib.lexers.shared_lex_rules as rule


LEX = LexBase()
LEX.lex_rules = [rule.shorthand, rule.number, rule.word, rule.sep]


class TestRange(unittest.TestCase):

    def compare_tokens(self, text, expect):
        tokens = LEX.tokenize(text)
        actual = [(t.token, text[t.start:t.end]) for t in tokens]
        self.assertEqual(actual, expect)

    def test_shorthand_01(self):
        text = '1-2-3-4'
        expect = [('shorthand', '1-2-3-4')]
        self.compare_tokens(text, expect)

    def test_shorthand_02(self):
        text = '1-2-3-4-5'
        expect = [('shorthand', '1-2-3-4-5')]
        self.compare_tokens(text, expect)

    def test_shorthand_03(self):
        text = '1-2-3-4-5-6'
        expect = [('number', '1'), ('number', '2'), ('number', '3'),
                  ('number', '4'), ('number', '5'), ('number', '6')]
        self.compare_tokens(text, expect)

    def test_shorthand_04(self):
        text = '1-2-3-4-5 g'
        expect = [('shorthand', '1-2-3-4-5 g')]
        self.compare_tokens(text, expect)

    def test_shorthand_05(self):
        text = '1-2-3-4-5g'
        expect = [('shorthand', '1-2-3-4-5g')]
        self.compare_tokens(text, expect)

    def test_shorthand_06(self):
        text = '1-2-3'
        expect = [('number', '1'), ('number', '2'), ('number', '3')]
        self.compare_tokens(text, expect)

    def test_shorthand_07(self):
        text = '1-2-3-4-'
        expect = [('number', '1'), ('number', '2'),
                  ('number', '3'), ('number', '4')]
        self.compare_tokens(text, expect)

    def test_shorthand_08(self):
        text = '-1-2-3-4'
        expect = [('number', '1'), ('number', '2'),
                  ('number', '3'), ('number', '4')]
        self.compare_tokens(text, expect)

    def test_shorthand_09(self):
        text = '1-2-3-4/'
        expect = [('number', '1'), ('number', '2'),
                  ('number', '3'), ('number', '4')]
        self.compare_tokens(text, expect)

    def test_shorthand_10(self):
        text = '1.1-2.2-33.3-4.4'
        expect = [('shorthand', '1.1-2.2-33.3-4.4')]
        self.compare_tokens(text, expect)

    def test_shorthand_11(self):
        text = '??-2.2-33.3-xx'
        expect = [('shorthand', '??-2.2-33.3-xx')]
        self.compare_tokens(text, expect)

    def test_shorthand_12(self):
        text = '??-2.2-33.3-44-xx'
        expect = [('shorthand', '??-2.2-33.3-44-xx')]
        self.compare_tokens(text, expect)

    def test_shorthand_13(self):
        text = '00 11-2.2-33.3-44-55 grams 99'
        expect = [('number', '00'), ('shorthand', '11-2.2-33.3-44-55 grams'),
                  ('number', '99')]
        self.compare_tokens(text, expect)

    def test_shorthand_14(self):
        text = '00 11-2.2-33.3-44=55 99'
        expect = [('number', '00'), ('shorthand', '11-2.2-33.3-44=55'),
                  ('number', '99')]
        self.compare_tokens(text, expect)

    def test_shorthand_15(self):
        text = '00 11-2.2-33.3-44/55 99'
        expect = [('number', '00'), ('shorthand', '11-2.2-33.3-44/55'),
                  ('number', '99')]
        self.compare_tokens(text, expect)

    def test_shorthand_16(self):
        text = '762-292-121-76 2435.0g'
        expect = [('shorthand', '762-292-121-76 2435.0g')]
        self.compare_tokens(text, expect)
