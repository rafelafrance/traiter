# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.base_lexer import BaseLexer


TKN = BaseLexer()


class TestBaseLexer(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            TKN.tokenize('strA=key1;'),
            [{'token': 'word', 'value': 'strA', 'start': 0, 'end': 4},
             {'token': 'word', 'value': 'key1', 'start': 5, 'end': 9},
             {'token': 'stop', 'value': ';', 'start': 9, 'end': 10}])

    def test_tokenize_02(self):
        self.assertEqual(
            TKN.tokenize('strA =key1;'),
            [{'token': 'word', 'value': 'strA', 'start': 0, 'end': 4},
             {'token': 'word', 'value': 'key1', 'start': 6, 'end': 10},
             {'token': 'stop', 'value': ';', 'start': 10, 'end': 11}])

    def test_tokenize_03(self):
        self.assertEqual(
            TKN.tokenize('strA= key1;'),
            [{'token': 'word', 'value': 'strA', 'start': 0, 'end': 4},
             {'token': 'word', 'value': 'key1', 'start': 6, 'end': 10},
             {'token': 'stop', 'value': ';', 'start': 10, 'end': 11}])

    def test_tokenize_04(self):
        self.assertEqual(
            TKN.tokenize('strA =  key1;'),
            [{'token': 'word', 'value': 'strA', 'start': 0, 'end': 4},
             {'token': 'word', 'value': 'key1', 'start': 8, 'end': 12},
             {'token': 'stop', 'value': ';', 'start': 12, 'end': 13}])

    def test_tokenize_05(self):
        self.assertEqual(
            TKN.tokenize('word1.word2'),
            [{'token': 'word', 'value': 'word1', 'start': 0, 'end': 5},
             {'token': 'stop', 'value': '.', 'start': 5, 'end': 6},
             {'token': 'word', 'value': 'word2', 'start': 6, 'end': 11}])

    def test_tokenize_06(self):
        self.assertEqual(
            TKN.tokenize('99mm'),
            [{'token': 'number', 'value': '99', 'start': 0, 'end': 2},
             {'token': 'word', 'value': 'mm', 'start': 2, 'end': 4}])

    def test_tokenize_07(self):
        self.assertEqual(
            TKN.tokenize(':99.5mm;'),
            [{'token': 'number', 'value': '99.5', 'start': 1, 'end': 5},
             {'token': 'word', 'value': 'mm', 'start': 5, 'end': 7},
             {'token': 'stop', 'value': ';', 'start': 7, 'end': 8}])
