# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
import lib.tokenizer as tk


class TestTokenizer(unittest.TestCase):

    def test_01(self):
        self.assertEqual(
            tk.tokenize('strA=key1;'),
            [(tk.WORD, 'strA', 0, 4),
             (tk.EQUAL, '=', 4, 5),
             (tk.WORD, 'key1', 5, 9),
             (tk.SEMI, ';', 9, 10)])

    def test_02(self):
        self.assertEqual(
            tk.tokenize('strA =key1;'),
            [(tk.WORD, 'strA', 0, 4),
             (tk.SPACES, ' ', 4, 5),
             (tk.EQUAL, '=', 5, 6),
             (tk.WORD, 'key1', 6, 10),
             (tk.SEMI, ';', 10, 11)])

    def test_03(self):
        self.assertEqual(
            tk.tokenize('strA= key1;'),
            [(tk.WORD, 'strA', 0, 4),
             (tk.EQUAL, '=', 4, 5),
             (tk.SPACES, ' ', 5, 6),
             (tk.WORD, 'key1', 6, 10),
             (tk.SEMI, ';', 10, 11)])

    def test_04(self):
        self.assertEqual(
            tk.tokenize('strA =  key1;'),
            [(tk.WORD, 'strA', 0, 4),
             (tk.SPACES, ' ', 4, 5),
             (tk.EQUAL, '=', 5, 6),
             (tk.SPACES, '  ', 6, 8),
             (tk.WORD, 'key1', 8, 12),
             (tk.SEMI, ';', 12, 13)])

    def test_05(self):
        self.assertEqual(
            tk.tokenize('word1.word2'),
            [(tk.WORD, 'word1', 0, 5),
             (tk.DOT, '.', 5, 6),
             (tk.WORD, 'word2', 6, 11)])

    def test_06(self):
        self.assertEqual(
            tk.tokenize('99mm'),
            [(tk.NUMBER, '99', 0, 2),
             (tk.WORD, 'mm', 2, 4)])

    def test_07(self):
        self.assertEqual(
            tk.tokenize(':99.5mm;'),
            [(tk.COLON, ':', 0, 1),
             (tk.NUMBER, '99.5', 1, 5),
             (tk.WORD, 'mm', 5, 7),
             (tk.SEMI, ';', 7, 8)])


SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestTokenizer)
unittest.TextTestRunner().run(SUITE)
