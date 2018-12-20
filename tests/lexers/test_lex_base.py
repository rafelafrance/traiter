# pylint: disable=missing-docstring,import-error,too-many-public-methods
# pylint: disable=global-statement,unused-argument

import unittest
from lib.lexers.lex_base import LexBase, Token
import lib.lexers.shared_lex_rules as rule


LEX = LexBase()


class TestBaseLexer(unittest.TestCase):

    def setup_method(self, method):
        global LEX
        del LEX.lex_rules
        LEX.lex_rules = [rule.number, rule.word, rule.stop]

    # #########################################################################

    def test_tokenize_01(self):
        self.assertEqual(
            LEX.tokenize('strA=key1;'),
            [Token(token='word', start=0, end=4),
             Token(token='word', start=5, end=9),
             Token(token='stop', start=9, end=10)])

    def test_tokenize_02(self):
        self.assertEqual(
            LEX.tokenize('strA =key1;'),
            [Token(token='word', start=0, end=4),
             Token(token='word', start=6, end=10),
             Token(token='stop', start=10, end=11)])

    def test_tokenize_03(self):
        self.assertEqual(
            LEX.tokenize('strA= key1;'),
            [Token(token='word', start=0, end=4),
             Token(token='word', start=6, end=10),
             Token(token='stop', start=10, end=11)])

    def test_tokenize_04(self):
        self.assertEqual(
            LEX.tokenize('strA =  key1;'),
            [Token(token='word', start=0, end=4),
             Token(token='word', start=8, end=12),
             Token(token='stop', start=12, end=13)])

    def test_tokenize_05(self):
        self.assertEqual(
            LEX.tokenize('word1.word2'),
            [Token(token='word', start=0, end=5),
             Token(token='stop', start=5, end=6),
             Token(token='word', start=6, end=11)])

    def test_tokenize_06(self):
        self.assertEqual(
            LEX.tokenize('99mm'),
            [Token(token='number', start=0, end=2)])

    def test_tokenize_07(self):
        self.assertEqual(
            LEX.tokenize(':99.5mm;'),
            [Token(token='number', start=1, end=5),
             Token(token='stop', start=7, end=8)])

    # #########################################################################

    def test_number_01(self):
        self.assertEqual(
            LEX.tokenize('0'),
            [Token(token='number', start=0, end=1)])

    def test_number_02(self):
        self.assertEqual(
            LEX.tokenize('1.'),
            [Token(token='number', start=0, end=1),
             Token(token='stop', start=1, end=2)])

    def test_number_03(self):
        self.assertEqual(
            LEX.tokenize('1.1'),
            [Token(token='number', start=0, end=3)])

    def test_number_04(self):
        self.assertEqual(
            LEX.tokenize('0.1'),
            [Token(token='number', start=0, end=3)])

    def test_number_05(self):
        self.assertEqual(
            LEX.tokenize('0,1'),
            [Token(token='number', start=0, end=1),
             Token(token='number', start=2, end=3)])

    def test_number_06(self):
        self.assertEqual(
            LEX.tokenize('12,3'),
            [Token(token='number', start=0, end=2),
             Token(token='number', start=3, end=4)])

    def test_number_07(self):
        self.assertEqual(
            LEX.tokenize('123,4'),
            [Token(token='number', start=0, end=3),
             Token(token='number', start=4, end=5)])

    def test_number_08(self):
        self.assertEqual(
            LEX.tokenize('1,234'),
            [Token(token='number', start=0, end=5)])

    def test_number_09(self):
        self.assertEqual(
            LEX.tokenize('1,234.'),
            [Token(token='number', start=0, end=5),
             Token(token='stop', start=5, end=6)])

    def test_number_10(self):
        self.assertEqual(
            LEX.tokenize('1,234.5'),
            [Token(token='number', start=0, end=7)])

    def test_number_11(self):
        self.assertEqual(
            LEX.tokenize('1,234.5.'),
            [Token(token='number', start=0, end=7),
             Token(token='stop', start=7, end=8)])

    def test_number_12(self):
        self.assertEqual(
            LEX.tokenize('1,234,5.'),
            [Token(token='number', start=0, end=5),
             Token(token='number', start=6, end=7),
             Token(token='stop', start=7, end=8)])

    def test_number_13(self):
        self.assertEqual(
            LEX.tokenize('12345'),
            [Token(token='number', start=0, end=5)])

    def test_number_14(self):
        self.assertEqual(
            LEX.tokenize('12345.'),
            [Token(token='number', start=0, end=5),
             Token(token='stop', start=5, end=6)])

    def test_number_15(self):
        self.assertEqual(
            LEX.tokenize('12345.6'),
            [Token(token='number', start=0, end=7)])

    # #########################################################################

    def test_range_01(self):
        global LEX
        del LEX.lex_rules
        LEX.lex_rules = [rule.range, rule.word, rule.stop]

        self.assertEqual(
            LEX.tokenize('12345.6'),
            [Token(token='range', start=0, end=7)])
