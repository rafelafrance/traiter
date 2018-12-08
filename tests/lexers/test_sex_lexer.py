# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.sex_lexer import SexLexer


TKN = SexLexer()


class TestSexLexer(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            #            0123456789.123456789.123456789.123456789.123456789.123
            TKN.tokenize('weight; sex=female ? ; age'),
            [{'token': 'word', 'value': 'weight', 'start': 0, 'end': 6},
             {'token': 'stop', 'value': ';', 'start': 6, 'end': 7},
             {'token': 'key', 'value': 'sex', 'start': 8, 'end': 11},
             {'token': 'sex', 'value': 'female', 'start': 12, 'end': 18},
             {'token': 'quest', 'value': '?', 'start': 19, 'end': 20},
             {'token': 'stop', 'value': ';', 'start': 21, 'end': 22},
             {'token': 'word', 'value': 'age', 'start': 23, 'end': 26}])

    def test_tokenize_02(self):
        self.assertEqual(
            #            0123456789.123456789.123456789.123456789.123456789.123
            TKN.tokenize('sex and age'),
            [{'token': 'key', 'value': 'sex', 'start': 0, 'end': 3},
             {'token': 'skip', 'value': 'and', 'start': 4, 'end': 7},
             {'token': 'word', 'value': 'age', 'start': 8, 'end': 11}])
