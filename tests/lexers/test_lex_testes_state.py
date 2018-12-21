import unittest
from lib.lexers.lex_base import Token
from lib.lexers.lex_testes_state import LexTestesState


LEX = LexTestesState()


class TestTestesStateLexer(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            LEX.tokenize('testes descended'),
            [Token(token='testes', start=0, end=6),
             Token(token='descended', start=7, end=16)])

    def test_tokenize_02(self):
        self.assertEqual(
            LEX.tokenize('testes undescended'),
            [Token(token='testes', start=0, end=6),
             Token(token='descended', start=7, end=18)])

    def test_tokenize_03(self):
        self.assertEqual(
            LEX.tokenize('testis undesc.'),
            [Token(token='testes', start=0, end=6),
             Token(token='descended', start=7, end=13),
             Token(token='sep', start=13, end=14)])

    def test_tokenize_04(self):
        self.assertEqual(
            LEX.tokenize('testicles undesc'),
            [Token(token='testes', start=0, end=9),
             Token(token='descended', start=10, end=16)])

    def test_tokenize_05(self):
        self.assertEqual(
            LEX.tokenize('testes not fully descended'),
            [Token(token='testes', start=0, end=6),
             Token(token='not', start=7, end=10),
             Token(token='fully', start=11, end=16),
             Token(token='descended', start=17, end=26)])

    def test_tokenize_06(self):
        self.assertEqual(
            LEX.tokenize('testes non-scrotal'),
            [Token(token='testes', start=0, end=6),
             Token(token='not', start=7, end=10),
             Token(token='scrotal', start=11, end=18)])

    def test_tokenize_07(self):
        self.assertEqual(
            LEX.tokenize('testes no scrotum'),
            [Token(token='testes', start=0, end=6),
             Token(token='not', start=7, end=9),
             Token(token='scrotal', start=10, end=17)])

    def test_tokenize_08(self):
        self.assertEqual(
            LEX.tokenize('testes nscr'),
            [Token(token='testes', start=0, end=6),
             Token(token='other_words', start=7, end=11)])

    def test_tokenize_09(self):
        self.assertEqual(
            LEX.tokenize('tes ns'),
            [Token(token='abbrev', start=0, end=3),
             Token(token='state_abbrev', start=4, end=6)])

    def test_tokenize_10(self):
        self.assertEqual(
            LEX.tokenize('tes undescend.'),
            [Token(token='abbrev', start=0, end=3),
             Token(token='descended', start=4, end=13),
             Token(token='sep', start=13, end=14)])

    def test_tokenize_11(self):
        self.assertEqual(
            LEX.tokenize('t abdominal'),
            [Token(token='abbrev', start=0, end=1),
             Token(token='abdominal', start=2, end=11)])

    def test_tokenize_12(self):
        self.assertEqual(
            LEX.tokenize('t nscr'),
            [Token(token='abbrev', start=0, end=1),
             Token(token='other_words', start=2, end=6)])

    def test_tokenize_13(self):
        self.assertEqual(
            LEX.tokenize('t ns'),
            [Token(token='abbrev', start=0, end=1),
             Token(token='state_abbrev', start=2, end=4)])
