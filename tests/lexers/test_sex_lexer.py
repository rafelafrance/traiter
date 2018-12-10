# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.sex_lexer import SexLexer


LEX = SexLexer()


class TestSexLexer(unittest.TestCase):

    def test_tokenize_01(self):
        self.maxDiff = None
        self.assertEqual(
            #             0123456789.123456789.123456789.123456789.123456789.12
            LEX.tokenize('sex male males female females ? and is was ; other'),
            [{'token': 'key', 'value': 'sex', 'start': 0, 'end': 3},
             {'token': 'sex', 'value': 'male', 'start': 4, 'end': 8},
             {'token': 'sex', 'value': 'males', 'start': 9, 'end': 14},
             {'token': 'sex', 'value': 'female', 'start': 15, 'end': 21},
             {'token': 'sex', 'value': 'females', 'start': 22, 'end': 29},
             {'token': 'quest', 'value': '?', 'start': 30, 'end': 31},
             {'token': 'skip', 'value': 'and', 'start': 32, 'end': 35},
             {'token': 'skip', 'value': 'is', 'start': 36, 'end': 38},
             {'token': 'skip', 'value': 'was', 'start': 39, 'end': 42},
             {'token': 'stop', 'value': ';', 'start': 43, 'end': 44},
             {'token': 'word', 'value': 'other', 'start': 45, 'end': 50}])
