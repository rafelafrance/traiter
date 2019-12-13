"""Test the replacer function in the parser module."""

import unittest
import regex
from pylib.stacked_regex.rule import replacer, vocab
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.parser import Parser


class TestReplace(unittest.TestCase):
    """Test the replacer function in the parser module."""

    flags = regex.VERBOSE | regex.IGNORECASE

    k_zero = vocab('zero', r' zero ')
    k_one = vocab('one', r' one ')
    k_two = vocab('two', r' two ')
    rules = [k_zero, k_one, k_two]

    def test_replace_01(self):
        """It replaces a token."""
        r_replace = replacer('replace', 'one')
        parser = Parser(self.rules + [r_replace])
        parser.build()
        text = 'ONE'
        t_one = Token(self.k_one, span=(0, 3), groups={'one': 'ONE'})
        self.assertEqual(
            parser.replace([t_one], text),
            ([Token(r_replace, span=(0, 3),
                    groups={'replace': 'ONE', 'one': 'ONE'})],
             True))

    def test_replace_02(self):
        """It replaces two tokens."""
        text = 'ONE TWO'
        t_one = Token(self.k_one, span=(0, 3), groups={'one': 'ONE'})
        t_two = Token(self.k_two, span=(4, 7), groups={'two': 'TWO'})
        r_replace = replacer('replace', r' one two ')
        parser = Parser(self.rules + [r_replace])
        parser.build()
        self.assertEqual(
            parser.replace([t_one, t_two], text),
            ([Token(
                r_replace, span=(0, 7),
                groups={'one': 'ONE', 'two': 'TWO', 'replace': 'ONE TWO'})],
             True))

    def test_replace_03(self):
        """It handles extra tokens."""
        text = 'ZERO ONE TWO ZERO'
        t_zero1 = Token(self.k_zero, span=(0, 4), groups={'zero': 'ZERO'})
        t_one = Token(self.k_one, span=(5, 8), groups={'one': 'ONE'})
        t_two = Token(self.k_two, span=(9, 12), groups={'two': 'TWO'})
        t_zero2 = Token(self.k_zero, span=(13, 17), groups={'zero': 'ZERO'})
        r_replace = replacer('replace', r' one two ')
        parser = Parser(self.rules + [r_replace])
        parser.build()
        self.assertEqual(
            parser.replace([t_zero1, t_one, t_two, t_zero2], text),
            ([
                Token(t_zero1, span=(0, 4), groups={'zero': 'ZERO'}),
                Token(
                    r_replace, span=(5, 12),
                    groups={'one': 'ONE', 'two': 'TWO', 'replace': 'ONE TWO'}),
                Token(t_zero2, span=(13, 17), groups={'zero': 'ZERO'})],
             True))

    def test_replace_04(self):
        """It handles tokens in the middle."""
        text = 'ONE ZERO TWO'
        t_one = Token(self.k_one, span=(0, 3), groups={'one': 'ONE'})
        t_zero = Token(self.k_zero, span=(4, 8), groups={'zero': 'ZERO'})
        t_two = Token(self.k_two, span=(9, 12), groups={'two': 'TWO'})
        r_replace = replacer('replace', r' one two ')
        parser = Parser(self.rules + [r_replace])
        parser.build()
        self.assertEqual(
            parser.replace([t_one, t_zero, t_two], text),
            ([
                Token(t_one, span=(0, 3), groups={'one': 'ONE'}),
                Token(t_zero, span=(4, 8), groups={'zero': 'ZERO'}),
                Token(t_two, span=(9, 12), groups={'two': 'TWO'})],
             False))
