# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.lex_base import Token
from lib.lexers.lex_sex import LexSex


LEX = LexSex()


class TestSexLexer(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            #             0123456789.123456789.123456789.123456789.123456789.12
            LEX.tokenize('sex male males female females ? and is was ; other'),
            [Token(token='key', start=0, end=3),
             Token(token='sex', start=4, end=8),
             Token(token='sex', start=9, end=14),
             Token(token='sex', start=15, end=21),
             Token(token='sex', start=22, end=29),
             Token(token='quest', start=30, end=31),
             Token(token='skip', start=32, end=35),
             Token(token='skip', start=36, end=38),
             Token(token='skip', start=39, end=42),
             Token(token='stop', start=43, end=44),
             Token(token='word', start=45, end=50)])
