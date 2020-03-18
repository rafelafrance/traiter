"""Test match function."""

import unittest
from traiter.new.rules.literals import Literals
from traiter.new.token import Token
from traiter.new.matcher import match, Match


class TestLiterals(unittest.TestCase):
    """Test literal matches."""

    def test_match_01(self):
        """It finds a match."""
        rule0 = Literals(literals=[['one']])
        patterns = [[rule0]]
        tokens = [Token('zero'), Token('one'), Token('two')]
        actual = match(patterns, tokens)
        expect = [
            Match(pattern_idx=0, token_start=1, token_end=2,
                  token2rule=[rule0]),
        ]
        self.assertEqual(actual, expect)

    def test_match_02(self):
        """It finds a match a second pattern."""
        rule0 = Literals(literals=[['0']])
        rule1 = Literals(literals=[['one']])
        patterns = [[rule0], [rule1]]
        tokens = [Token('zero'), Token('one'), Token('two')]
        actual = match(patterns, tokens)
        expect = [
            Match(pattern_idx=1, token_start=1, token_end=2,
                  token2rule=[rule1]),
        ]
        self.assertEqual(actual, expect)

    def test_match_03(self):
        """It finds a two rule match."""
        rule0 = Literals(literals=[['0']])
        rule1 = Literals(literals=[['one']])
        rule2 = Literals(literals=[['two']])
        patterns = [[rule0], [rule1, rule2]]
        tokens = [Token('zero'), Token('one'), Token('two'), Token('three')]
        actual = match(patterns, tokens)
        expect = [
            Match(pattern_idx=1, token_start=1, token_end=3,
                  token2rule=[rule1, rule2]),
        ]
        self.assertEqual(actual, expect)

    def test_match_04(self):
        """It finds a multiple matches."""
        rule0 = Literals(literals=[['0']])
        rule1 = Literals(literals=[['one']])
        rule3 = Literals(literals=[['three']])
        patterns = [[rule0], [rule1], [rule3]]
        tokens = [Token('zero'), Token('one'), Token('two'), Token('three')]
        actual = match(patterns, tokens)
        expect = [
            Match(pattern_idx=1, token_start=1, token_end=2,
                  token2rule=[rule1]),
            Match(pattern_idx=2, token_start=3, token_end=4,
                  token2rule=[rule3]),
        ]
        self.assertEqual(actual, expect)
