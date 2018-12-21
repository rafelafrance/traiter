# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.lex_base import Token
from lib.lexers.lex_life_stage import LexLifeStage


LEX = LexLifeStage()


class TestLifeStageLexer(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            LEX.tokenize('lifestage life stage lifestage remarks'),
            [Token(token='key', start=0, end=9),
             Token(token='key', start=10, end=20),
             Token(token='key', start=21, end=38)])

    def test_tokenize_02(self):
        self.assertEqual(
            LEX.tokenize('ageclass age class ageinhours age in days age'),
            [Token(token='key', start=0, end=8),
             Token(token='key', start=9, end=18),
             Token(token='key', start=19, end=29),
             Token(token='key', start=30, end=41),
             Token(token='key', start=42, end=45)])

    def test_tokenize_03(self):
        self.assertEqual(
            LEX.tokenize(';,"'),
            [Token(token='sep', start=0, end=1),
             Token(token='sep', start=1, end=2),
             Token(token='sep', start=2, end=3)])

    def test_tokenize_04(self):
        self.assertEqual(
            LEX.tokenize('year first year second year after hatching    year'),
            [Token(token='word_plus', start=0, end=4),
             Token(token='keyless', start=5, end=15),
             Token(token='keyless', start=16, end=27),
             Token(token='keyless', start=28, end=50)])

    def test_tokenize_05(self):
        self.assertEqual(
            LEX.tokenize('yolksac yolk sac embryo'),
            [Token(token='keyless', start=0, end=7),
             Token(token='keyless', start=8, end=16),
             Token(token='word_plus', start=17, end=23)])

    def test_tokenize_06(self):
        self.assertEqual(
            LEX.tokenize('age class=over-winter ;'),
            [Token(token='key', start=0, end=9),
             Token(token='word_plus', start=10, end=21),
             Token(token='sep', start=22, end=23)])

    def test_tokenize_07(self):
        self.assertEqual(
            #             0123456789.123456789.1234567
            LEX.tokenize('LifeStage Remarks: 5-6 wks'),
            [Token(token='key', start=0, end=17),
             Token(token='word_plus', start=19, end=22),
             Token(token='word_plus', start=23, end=26)])

    def test_tokenize_08(self):
        self.assertEqual(
            #             0123456789.123456789.1234567
            LEX.tokenize('age=u ad.'),
            [Token(token='key', start=0, end=3),
             Token(token='word_plus', start=4, end=5),
             Token(token='keyless', start=6, end=8)])
