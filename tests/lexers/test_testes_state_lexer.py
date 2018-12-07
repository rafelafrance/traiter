# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.testes_state_lexer import LexerTestesState


class TestTestesStateLexer(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            TK.tokenize('testes descended'),
            [{'token': 'testes', 'value': 'testes', 'start': 0, 'end': 6},
             {'token': 'descended',
              'value': 'descended',
              'start': 7,
              'end': 16}])

    def test_tokenize_02(self):
        self.assertEqual(
            TK.tokenize('testes undescended'),
            [{'token': 'testes', 'value': 'testes', 'start': 0, 'end': 6},
             {'token': 'descended',
              'value': 'undescended',
              'start': 7,
              'end': 18}])

    def test_tokenize_03(self):
        self.assertEqual(
            TK.tokenize('testis undesc.'),
            [{'token': 'testes', 'value': 'testis', 'start': 0, 'end': 6},
             {'token': 'descended', 'value': 'undesc', 'start': 7, 'end': 13},
             {'token': 'stop', 'value': '.', 'start': 13, 'end': 14}])

    def test_tokenize_04(self):
        self.assertEqual(
            TK.tokenize('testicles undesc'),
            [{'token': 'testes', 'value': 'testicles', 'start': 0, 'end': 9},
             {'token': 'descended',
              'value': 'undesc',
              'start': 10,
              'end': 16}])

    def test_tokenize_05(self):
        self.assertEqual(
            TK.tokenize('testes not fully descended'),
            [{'token': 'testes', 'value': 'testes', 'start': 0, 'end': 6},
             {'token': 'not', 'value': 'not', 'start': 7, 'end': 10},
             {'token': 'fully', 'value': 'fully', 'start': 11, 'end': 16},
             {'token': 'descended',
              'value': 'descended',
              'start': 17,
              'end': 26}])

    def test_tokenize_06(self):
        self.assertEqual(
            TK.tokenize('testes non-scrotal'),
            [{'token': 'testes', 'value': 'testes', 'start': 0, 'end': 6},
             {'token': 'not', 'value': 'non', 'start': 7, 'end': 10},
             {'token': 'scrotal', 'value': 'scrotal', 'start': 11, 'end': 18}])

    def test_tokenize_07(self):
        self.assertEqual(
            TK.tokenize('testes no scrotum'),
            [{'token': 'testes', 'value': 'testes', 'start': 0, 'end': 6},
             {'token': 'not', 'value': 'no', 'start': 7, 'end': 9},
             {'token': 'scrotal', 'value': 'scrotum', 'start': 10, 'end': 17}])

    def test_tokenize_08(self):
        self.assertEqual(
            TK.tokenize('testes nscr'),
            [{'token': 'testes', 'value': 'testes', 'start': 0, 'end': 6},
             {'token': 'other_words', 'value': 'nscr', 'start': 7, 'end': 11}])

    def test_tokenize_09(self):
        self.assertEqual(
            TK.tokenize('tes ns'),
            [{'token': 'abbrev', 'value': 'tes', 'start': 0, 'end': 3},
             {'token': 'state_abbrev', 'value': 'ns', 'start': 4, 'end': 6}])

    def test_tokenize_10(self):
        self.assertEqual(
            TK.tokenize('tes undescend.'),
            [{'token': 'abbrev', 'value': 'tes', 'start': 0, 'end': 3},
             {'token': 'descended',
              'value': 'undescend',
              'start': 4,
              'end': 13},
             {'token': 'stop', 'value': '.', 'start': 13, 'end': 14}])

    def test_tokenize_11(self):
        self.assertEqual(
            TK.tokenize('t abdominal'),
            [{'token': 'abbrev', 'value': 't', 'start': 0, 'end': 1},
             {'token': 'abdominal',
              'value': 'abdominal',
              'start': 2,
              'end': 11}])

    def test_tokenize_12(self):
        self.assertEqual(
            TK.tokenize('t nscr'),
            [{'token': 'abbrev', 'value': 't', 'start': 0, 'end': 1},
             {'token': 'other_words', 'value': 'nscr', 'start': 2, 'end': 6}])

    def test_tokenize_13(self):
        self.assertEqual(
            TK.tokenize('t ns'),
            [{'token': 'abbrev', 'value': 't', 'start': 0, 'end': 1},
             {'token': 'state_abbrev', 'value': 'ns', 'start': 2, 'end': 4}])


TK = LexerTestesState()
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestTestesStateLexer)
unittest.TextTestRunner().run(SUITE)
