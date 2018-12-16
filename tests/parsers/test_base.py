# pylint: disable=missing-docstring,import-error,too-many-public-methods
# pylint: disable=global-statement,unused-argument

import unittest
from lib.lexers.lex_base import LexBase, Token
from lib.parsers.parse_base import ParseBase, Action
from lib.parsers.reducers import Result, value_span

PAR = None


class MockParser(ParseBase):

    def __init__(self):
        super().__init__(LexBase)

    def rule_dict(self):
        return {
            'word   to   word': Action(replace='len_width'),
            'number   to   number': Action(replace='range'),
            'cross': Action(replace='1_cross'),
            'cross   cross': Action(replace='2_crosses'),
            'cross   number': Action(replace='by_num'),
            'cross   cross cross': Action(replace='3_crosses'),
        }


def setup_module(module):
    global PAR
    PAR = MockParser()


class TestParseBase(unittest.TestCase):

    def test_build_rules_01(self):
        self.assertEqual(
            PAR.rules,
            {
                'word to word': Action(replace='len_width', len=3),
                'number to number': Action(replace='range', len=3),
                'cross': Action(replace='1_cross', len=1),
                'cross cross': Action(replace='2_crosses', len=2),
                'cross number': Action(replace='by_num', len=2),
                'cross cross cross': Action(replace='3_crosses', len=3),
            })

    def test_find_longest_match_01(self):
        PAR.stack = [
            Token(token='number', start=0, end=0),
            Token(token='to', start=0, end=0),
            Token(token='number', start=0, end=0)]
        self.assertEqual(
            PAR.find_longest_match(),
            ('number to number', Action(replace='range', len=3)))

    def test_find_longest_match02(self):
        PAR.stack = [Token(token='number', start=0, end=0),
                     Token(token='to', start=0, end=0)]
        self.assertEqual(PAR.find_longest_match(), (None, None))

    def test_find_longest_match_03(self):
        PAR.stack = [Token(token='number', start=0, end=0),
                     Token(token='to', start=0, end=0),
                     Token(token='number', start=0, end=0),
                     Token(token='to', start=0, end=0),
                     Token(token='number', start=0, end=0)]
        self.assertEqual(
            PAR.find_longest_match(),
            ('number to number', Action(replace='range', len=3)))

    def test_shift_01(self):
        PAR.stack = [1, 2, 3]
        PAR.tokens = [4, 5, 6]
        PAR.shift()
        self.assertEqual(PAR.stack, [1, 2, 3, 4])
        self.assertEqual(PAR.tokens, [5, 6])

    def test_replace_01(self):
        # reduce to token
        #      0123456789.123456789.123456789.12
        PAR.stack = [
            Token(token='one', start=7, end=10),
            Token(token='cross', start=11, end=12),
            Token(token='cross', start=14, end=14),
        ]
        results = []
        prod = Action(replace='2_crosses', len=2)
        PAR.replace(prod)
        self.assertEqual(
            PAR.stack,
            [Token(token='one', start=7, end=10),
             Token(token='2_crosses', start=11, end=14)])
        self.assertEqual(results, [])

    def test_reduce_02(self):
        # reduce to function
        #      0123456789.123456789.123456789.12
        raw = 'before one x x after'
        PAR.stack = [
            Token(token='one', start=7, end=10),
            Token(token='cross', start=11, end=12),
            Token(token='cross', start=14, end=14),
        ]
        results = []
        prod = Action(reduce=value_span, args={'span': (0, 1)}, len=2)

        PAR.reduce(raw, results, prod)
        self.assertEqual(
            PAR.stack, [Token(token='one', start=7, end=10)])
        self.assertEqual(results, [Result(value='x x', start=11, end=14)])

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
