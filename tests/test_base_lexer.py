# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.base_lexer import BaseLexer


class TestBaseLexer(unittest.TestCase):

    def test_01(self):
        self.assertEqual(
            TK.tokenize('strA=key1;'),
            [('word', 'strA', 0, 4),
             ('word', 'key1', 5, 9)])

    def test_02(self):
        self.assertEqual(
            TK.tokenize('strA =key1;'),
            [('word', 'strA', 0, 4),
             ('word', 'key1', 6, 10)])

    def test_03(self):
        self.assertEqual(
            TK.tokenize('strA= key1;'),
            [('word', 'strA', 0, 4),
             ('word', 'key1', 6, 10)])

    def test_04(self):
        self.assertEqual(
            TK.tokenize('strA =  key1;'),
            [('word', 'strA', 0, 4),
             ('word', 'key1', 8, 12)])

    def test_05(self):
        self.assertEqual(
            TK.tokenize('word1.word2'),
            [('word', 'word1', 0, 5),
             ('word', 'word2', 6, 11)])

    def test_06(self):
        self.assertEqual(
            TK.tokenize('99mm'),
            [('number', '99', 0, 2),
             ('word', 'mm', 2, 4)])

    def test_07(self):
        self.assertEqual(
            TK.tokenize(':99.5mm;'),
            [('number', '99.5', 1, 5),
             ('word', 'mm', 5, 7)])


TK = BaseLexer()
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestBaseLexer)
unittest.TextTestRunner().run(SUITE)
