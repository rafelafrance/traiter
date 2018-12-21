import unittest
from lib.lexers.lex_base import LexBase, Token
from lib.parsers.parse_base import ParseBase, Action
from lib.parsers.shared_reducers import Result, value_span
import lib.lexers.shared_regexp as rule


PAR = None


class MockLexer(LexBase):
    def rule_list(self):
        return [rule.get('number'), rule.get('word'), rule.get('sep')]


class MockParser(ParseBase):

    def rule_dict(self):
        return {
            ' word  ': Action(replace='word_1'),
            'word      word': Action(replace='words_2'),
            'word      word word': Action(replace='words_3'),
            'number    number': Action(replace='numbers_2'),
            'word      number': Action(replace='word_number'),
        }


def setup_module(module):
    global PAR
    PAR = MockParser(MockLexer)


class TestParseBase(unittest.TestCase):

    def test_build_rules_01(self):
        self.assertEqual(
            PAR.rules,
            {
                'word': Action(replace='word_1', len=1),
                'word word': Action(replace='words_2', len=2),
                'word word word': Action(replace='words_3', len=3),
                'number number': Action(replace='numbers_2', len=2),
                'word number': Action(replace='word_number', len=2),
            })

    def test_find_longest_match_01(self):
        PAR.stack = [
            Token(token='sep', start=0, end=0),
            Token(token='number', start=0, end=0),
            Token(token='number', start=0, end=0),
            Token(token='number', start=0, end=0)]
        self.assertEqual(
            PAR.find_longest_match(),
            ('number number', Action(replace='numbers_2', len=2)))

    def test_find_longest_match_02(self):
        PAR.stack = [Token(token='number', start=0, end=0),
                     Token(token='to', start=0, end=0)]
        self.assertEqual(PAR.find_longest_match(), (None, None))

    def test_find_longest_match_03(self):
        PAR.stack = [Token(token='number', start=0, end=0),
                     Token(token='sep', start=0, end=0),
                     Token(token='number', start=0, end=0),
                     Token(token='number', start=0, end=0)]
        self.assertEqual(
            PAR.find_longest_match(),
            ('number number', Action(replace='numbers_2', len=2)))

    def test_shift_01(self):
        PAR.stack = [1, 2, 3]
        PAR.tokens = [4, 5, 6]
        PAR.shift()
        self.assertEqual(PAR.stack, [1, 2, 3, 4])
        self.assertEqual(PAR.tokens, [5, 6])

    def test_replace_01(self):
        PAR.stack = [
            Token(token='one', start=7, end=10),
            Token(token='word', start=11, end=12),
            Token(token='word', start=14, end=14),
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
        raw = 'before one x x after'
        PAR.stack = [
            Token(token='one', start=7, end=10),
            Token(token='word', start=11, end=12),
            Token(token='word', start=14, end=14),
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
            {'number': [(2, 0), (1, 1)],
             'word': [(3, 0), (2, 1), (1, 2), (2, 0), (1, 1), (1, 0)]})
