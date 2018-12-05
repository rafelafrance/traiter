# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.testes_state_lexer import LexerTestesState


class TestTestesStateLexer(unittest.TestCase):

    def test_01(self):
        self.assertEqual(
            TK.tokenize('testes descended'),
            [('testes', 'testes', 0, 6),
             ('descended', 'descended', 7, 16)])

    def test_02(self):
        self.assertEqual(
            TK.tokenize('testes undescended'),
            [('testes', 'testes', 0, 6),
             ('descended', 'undescended', 7, 18)])

    def test_03(self):
        self.assertEqual(
            TK.tokenize('testis undesc.'),
            [('testes', 'testis', 0, 6),
             ('descended', 'undesc', 7, 13)])

    def test_04(self):
        self.assertEqual(
            TK.tokenize('testicles undesc'),
            [('testes', 'testicles', 0, 9),
             ('descended', 'undesc', 10, 16)])

    def test_05(self):
        self.assertEqual(
            TK.tokenize('testes not fully descended'),
            [('testes', 'testes', 0, 6),
             ('not', 'not', 7, 10),
             ('fully', 'fully', 11, 16),
             ('descended', 'descended', 17, 26)])

    def test_06(self):
        self.assertEqual(
            TK.tokenize('testes not-scrotal'),
            [('testes', 'testes', 0, 6),
             ('not', 'not', 7, 10),
             ('scrotal', 'scrot', 11, 16)])

    def test_07(self):
        self.assertEqual(
            TK.tokenize('testes no scrotum'),
            [('testes', 'testes', 0, 6),
             ('not', 'no', 7, 9),
             ('scrotal', 'scrot', 10, 15)])

    def test_08(self):
        self.assertEqual(
            TK.tokenize('testes nscr'),
            [('testes', 'testes', 0, 6),
             ('other_words', 'nscr', 7, 11)])

    def test_09(self):
        self.assertEqual(
            TK.tokenize('tes ns'),
            [('testes_abbrev', 'tes', 0, 3),
             ('state_abbrev', 'ns', 4, 6)])

    def test_10(self):
        self.assertEqual(
            TK.tokenize('tes undescend.'),
            [('testes_abbrev', 'tes', 0, 3),
             ('descended', 'undescend', 4, 13)])

    def test_11(self):
        self.assertEqual(
            TK.tokenize('t abdominal'),
            [('testes_abbrev', 't', 0, 1),
             ('key_req', 'abdominal', 2, 11)])

    def test_12(self):
        self.assertEqual(
            TK.tokenize('t nscr'),
            [('testes_abbrev', 't', 0, 1),
             ('other_words', 'nscr', 2, 6)])

    def test_13(self):
        self.assertEqual(
            TK.tokenize('t ns'),
            [('testes_abbrev', 't', 0, 1),
             ('state_abbrev', 'ns', 2, 4)])


TK = LexerTestesState()
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestTestesStateLexer)
unittest.TextTestRunner().run(SUITE)
