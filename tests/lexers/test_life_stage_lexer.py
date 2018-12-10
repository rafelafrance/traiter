# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.life_stage_lexer import LifeStageLexer


LEX = LifeStageLexer()


class TestLifeStageLexer(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            LEX.tokenize('lifestage life stage lifestage remarks'),
            [{'token': 'key', 'value': 'lifestage', 'start': 0, 'end': 9},
             {'token': 'key', 'value': 'life stage', 'start': 10, 'end': 20},
             {'token': 'key', 'value': 'lifestage remarks',
              'start': 21, 'end': 38},
             {'end': 38, 'start': 38, 'token': 'stop', 'value': ''}])

    def test_tokenize_02(self):
        self.assertEqual(
            LEX.tokenize('ageclass age class ageinhours age in days age'),
            [{'token': 'key', 'value': 'ageclass', 'start': 0, 'end': 8},
             {'token': 'key', 'value': 'age class', 'start': 9, 'end': 18},
             {'token': 'key', 'value': 'ageinhours', 'start': 19, 'end': 29},
             {'token': 'key', 'value': 'age in days', 'start': 30, 'end': 41},
             {'token': 'key', 'value': 'age', 'start': 42, 'end': 45},
             {'end': 45, 'start': 45, 'token': 'stop', 'value': ''}])

    def test_tokenize_03(self):
        self.assertEqual(
            LEX.tokenize(';,"'),
            [{'token': 'stop', 'value': ';', 'start': 0, 'end': 1},
             {'token': 'stop', 'value': ',', 'start': 1, 'end': 2},
             {'token': 'stop', 'value': '"', 'start': 2, 'end': 3},
             {'end': 3, 'start': 3, 'token': 'stop', 'value': ''}])

    def test_tokenize_04(self):
        self.assertEqual(
            LEX.tokenize('year first year second year after hatching    year'),
            [{'end': 4, 'start': 0, 'token': 'word_plus', 'value': 'year'},
             {'token': 'keyless', 'value': 'first year',
              'start': 5, 'end': 15},
             {'token': 'keyless', 'value': 'second year',
              'start': 16, 'end': 27},
             {'token': 'keyless', 'value': 'after hatching    year',
              'start': 28, 'end': 50},
             {'end': 50, 'start': 50, 'token': 'stop', 'value': ''}])

    def test_tokenize_05(self):
        self.assertEqual(
            LEX.tokenize('yolksac yolk sac embryo'),
            [{'token': 'before_birth', 'value': 'yolksac',
              'start': 0, 'end': 7},
             {'token': 'before_birth', 'value': 'yolk sac',
              'start': 8, 'end': 16},
             {'token': 'word_plus', 'value': 'embryo',
              'start': 17, 'end': 23},
             {'end': 23, 'start': 23, 'token': 'stop', 'value': ''}])

    def test_tokenize_06(self):
        self.assertEqual(
            #             0123456789.123456789.123
            LEX.tokenize('age class=over-winter ;'),
            [{'token': 'key', 'value': 'age class', 'start': 0, 'end': 9},
             {'token': 'word_plus', 'value': 'over-winter',
              'start': 10, 'end': 21},
             {'end': 23, 'start': 22, 'token': 'stop', 'value': ';'},
             {'end': 23, 'start': 23, 'token': 'stop', 'value': ''}])
