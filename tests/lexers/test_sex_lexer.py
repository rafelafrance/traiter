# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.lexers.sex_lexer import SexLexer


class TestSexLexer(unittest.TestCase):

    def test_tokenize_01(self):
        self.assertEqual(
            #            0123456789.123456789.123456789.123456789.123456789.123
            TK.tokenize('weight; sex=female ? ; age'),
            [{'token': 'limited', 'value': 'weight', 'start': 0, 'end': 6},
             {'token': 'stop', 'value': ';', 'start': 6, 'end': 7},
             {'token': 'key', 'value': 'sex', 'start': 8, 'end': 11},
             {'token': 'sex', 'value': 'female', 'start': 12, 'end': 18},
             {'token': 'quest', 'value': '?', 'start': 19, 'end': 20},
             {'token': 'stop', 'value': ';', 'start': 21, 'end': 22},
             {'token': 'limited', 'value': 'age', 'start': 23, 'end': 26}])


TK = SexLexer()
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestSexLexer)
unittest.TextTestRunner().run(SUITE)
