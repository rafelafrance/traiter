# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.lex_base import Token
from lib.lexers.lex_total_length import LexTotalLength


LEX = LexTotalLength()


class TestLexTotalLength(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            LEX.tokenize('{"totalLengthInMM":"123" };'),
            [Token(token='key_with_units', start=2, end=17),
             Token(token='range', start=20, end=23),
             Token(token='stop', start=26, end=27)])

    def test_tokenize_02(self):
        self.assertEqual(
            LEX.tokenize('"{"measurements":"308-190-45-20" }"'),
            [Token(token='shorthand_key', start=3, end=15),
             Token(token='shorthand', start=18, end=31)])

    def test_tokenize_03(self):
        self.assertEqual(
            #             0123456789.123456789.123456789.123456789.123456789.12
            LEX.tokenize('308-190-45-20'),
            [Token(token='shorthand', start=0, end=13)])

    def test_tokenize_04(self):
        self.maxDiff = None
        self.assertEqual(
            #             0123456789.123456789.123456789.123456789.123456789.12
            LEX.tokenize('t.l.= 2 feet 3.1 - 4.5 inches '),
            [Token(token='total_len_key', start=0, end=4),
             Token(token='range', start=6, end=7),
             Token(token='feet', start=8, end=12),
             Token(token='range', start=13, end=22),
             Token(token='inches', start=23, end=29)])
