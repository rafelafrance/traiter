import unittest
from lib.lexers.lex_base import LexBase, Token
import lib.lexers.shared_regexp as regexp


LEX = LexBase()
LEX.lex_rules = [regexp.number, regexp.word, regexp.sep]
LEX.build_regex()


class TestBaseLexer(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            LEX.tokenize('strA=key1;'),
            [Token(token='word', start=0, end=4),
             Token(token='word', start=5, end=9),
             Token(token='sep', start=9, end=10)])

    def test_tokenize_02(self):
        self.assertEqual(
            LEX.tokenize('strA =key1;'),
            [Token(token='word', start=0, end=4),
             Token(token='word', start=6, end=10),
             Token(token='sep', start=10, end=11)])

    def test_tokenize_03(self):
        self.assertEqual(
            LEX.tokenize('strA= key1;'),
            [Token(token='word', start=0, end=4),
             Token(token='word', start=6, end=10),
             Token(token='sep', start=10, end=11)])

    def test_tokenize_04(self):
        self.assertEqual(
            LEX.tokenize('strA =  key1;'),
            [Token(token='word', start=0, end=4),
             Token(token='word', start=8, end=12),
             Token(token='sep', start=12, end=13)])

    def test_tokenize_05(self):
        self.assertEqual(
            LEX.tokenize('word1.word2'),
            [Token(token='word', start=0, end=5),
             Token(token='sep', start=5, end=6),
             Token(token='word', start=6, end=11)])

    def test_tokenize_06(self):
        self.assertEqual(
            LEX.tokenize('99mm'),
            [Token(token='number', start=0, end=2)])

    def test_tokenize_07(self):
        self.assertEqual(
            LEX.tokenize(':99.5mm;'),
            [Token(token='number', start=1, end=5),
             Token(token='sep', start=7, end=8)])
