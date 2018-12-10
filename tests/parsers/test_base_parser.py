# pylint: disable=missing-docstring,import-error,too-many-public-methods
# pylint: disable=global-statement,unused-argument

import unittest
from lib.lexers.base_lexer import BaseLexer
from lib.parsers.base_parser import BaseParser
import lib.parsers.reducers as reduce

PAR = None


class MockParser(BaseParser):

    def __init__(self):
        super().__init__(BaseLexer)

    def rule_dict(self):
        return {
            'word   to   word': {'action': 'len_width'},
            'number   to   number': {'action': 'range'},
            'cross': {'action': '1_cross'},
            'cross   cross': {'action': '2_crosses'},
            'cross   number': {'action': 'by_num'},
            'cross   cross cross': {'action': '3_crosses'},
        }


def setup_module(module):
    global PAR
    PAR = MockParser()


class TestBaseParser(unittest.TestCase):

    def test_build_rules_01(self):
        self.assertEqual(
            PAR.rules,
            {
                'word to word': {'action': 'len_width', 'len': 3},
                'number to number': {'action': 'range', 'len': 3},
                'cross': {'action': '1_cross', 'len': 1},
                'cross cross': {'action': '2_crosses', 'len': 2},
                'cross number': {'action': 'by_num', 'len': 2},
                'cross cross cross': {'action': '3_crosses', 'len': 3},
            })

    def test_find_longest_match_01(self):
        PAR.stack = [
            {'token': 'number'}, {'token': 'to'}, {'token': 'number'}]
        self.assertEqual(
            PAR.find_longest_match(),
            ('number to number', {'action': 'range', 'len': 3}))

    def test_find_longest_match02(self):
        PAR.stack = [{'token': 'number'}, {'token': 'to'}]
        self.assertEqual(PAR.find_longest_match(), (None, None))

    def test_find_longest_match_03(self):
        PAR.stack = [{'token': 'number'}, {'token': 'to'},
                     {'token': 'number'}, {'token': 'to'},
                     {'token': 'number'}]
        self.assertEqual(
            PAR.find_longest_match(),
            ('number to number', {'action': 'range', 'len': 3}))

    def test_shift_01(self):
        PAR.stack = [1, 2, 3]
        PAR.tokens = [4, 5, 6]
        PAR.shift()
        self.assertEqual(PAR.stack, [1, 2, 3, 4])
        self.assertEqual(PAR.tokens, [5, 6])

    def test_reduce_01(self):
        # reduce to token
        #      0123456789.123456789.123456789.12
        raw = 'before one x x after'
        PAR.stack = [
            {'token': 'one', 'start': 7, 'end': 10},
            {'token': 'cross', 'start': 11, 'end': 12},
            {'token': 'cross', 'start': 14, 'end': 14},
        ]
        results = []
        prod = {'action': '2_crosses', 'len': 2}
        PAR.reduce(raw, results, prod)
        self.assertEqual(
            PAR.stack,
            [{'token': 'one', 'start': 7, 'end': 10},
             {'token': '2_crosses', 'start': 11, 'end': 14, 'value': 'x x'}])
        self.assertEqual(results, [])

    def test_reduce_02(self):
        # reduce to function
        #      0123456789.123456789.123456789.12
        raw = 'before one x x after'
        PAR.stack = [
            {'token': 'one', 'start': 7, 'end': 10},
            {'token': 'cross', 'start': 11, 'end': 12},
            {'token': 'cross', 'start': 14, 'end': 14},
        ]
        results = []
        prod = {
            'action': reduce.value_span,
            'args': {'span': (0, 1)},
            'len': 2}

        PAR.reduce(raw, results, prod)
        self.assertEqual(
            PAR.stack, [{'token': 'one', 'start': 7, 'end': 10}])
        self.assertEqual(results, [{'value': 'x x', 'start': 11, 'end': 14}])

    def test_post_process_01(self):
        results = ['test']
        self.assertEqual(PAR.post_process(results), results)

    def test_build_windows_01(self):
        self.assertEqual(
            PAR.build_windows(),
            {'cross': [(3, 0), (2, 1), (1, 2), (2, 0), (1, 1), (1, 0)],
             'number': [(3, 0), (1, 2), (2, 0)],
             'to': [(2, 1)],
             'word': [(3, 0), (1, 2)]})
