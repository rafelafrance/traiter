import re
import unittest
from pylib.stacked_regex.rule import replacer, keyword
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.parser import replace


class TestReplace(unittest.TestCase):

    flags = re.VERBOSE | re.IGNORECASE

    k_zero = keyword('zero', r' zero ')
    k_one = keyword('one', r' one ')
    k_two = keyword('two', r' two ')

    def test_replace_01(self):
        """It replaces a token."""
        text = 'ONE'
        t_one = Token(self.k_one, span=(0, 3), groups={'one': 'ONE'})
        r_replace = replacer('replace', r' one ')
        self.assertEqual(
            replace([r_replace], [t_one], text),
            ([Token(r_replace, span=(0, 3),
                    groups={'replace': 'ONE', 'one': 'ONE'})],
             True))

    def test_replace_02(self):
        """It replaces two tokens."""
        text = 'ONE TWO'
        t_one = Token(self.k_one, span=(0, 3), groups={'one': 'ONE'})
        t_two = Token(self.k_two, span=(4, 7), groups={'two': 'TWO'})
        r_replace = replacer('replace', r' one two ')
        self.assertEqual(
            replace([r_replace], [t_one, t_two], text),
            ([Token(
                r_replace, span=(0, 7),
                groups={'one': 'ONE', 'two': 'TWO', 'replace': 'ONE TWO'})],
             True))

    def test_replace_03(self):
        """It handles extra tokens."""
        self.maxDiff = None
        text = 'ZERO ONE TWO ZERO'
        t_zero1 = Token(self.k_zero, span=(0, 4), groups={'zero': 'ZERO'})
        t_one = Token(self.k_one, span=(5, 8), groups={'one': 'ONE'})
        t_two = Token(self.k_two, span=(9, 12), groups={'two': 'TWO'})
        t_zero2 = Token(self.k_zero, span=(13, 17), groups={'zero': 'ZERO'})
        r_replace = replacer('replace', r' one two ')
        self.assertEqual(
            replace([r_replace], [t_zero1, t_one, t_two, t_zero2], text),
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
        self.assertEqual(
            replace([r_replace], [t_one, t_zero, t_two], text),
            ([
                Token(t_one, span=(0, 3), groups={'one': 'ONE'}),
                Token(t_zero, span=(4, 8), groups={'zero': 'ZERO'}),
                Token(t_two, span=(9, 12), groups={'two': 'TWO'})],
                False))
