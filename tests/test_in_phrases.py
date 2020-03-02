"""Test the in_phrases rule."""

import unittest
from traiter.new.rules.in_phrases import InPhrases
from traiter.new.token import Token
from traiter.new.state import State


class TestInPhrases(unittest.TestCase):
    """Test the scanner'."""

    def test__init__01(self):
        """It builds phrases."""
        rule = InPhrases(phrases=[['one'], ['two'], ['three', 'four']])
        self.assertEqual(rule.values[0], (2, {('three', 'four')}))
        self.assertEqual(rule.values[1], (1, {('one', ), ('two', )}))

    def test_func_01(self):
        """It matches a token."""
        rule = InPhrases(phrases=[['one']])
        tokens = [Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(match_len=1))

    def test_func_02(self):
        """It matches two tokens."""
        rule = InPhrases(phrases=[['one', 'two']])
        tokens = [Token('one'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(match_len=2))

    def test_func_03(self):
        """It matches the second token."""
        rule = InPhrases(phrases=[['two']])
        tokens = [Token('one'), Token('two')]
        state = State(token_idx=1)
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(token_idx=1, match_len=1))

    def test_func_04(self):
        """It does not match after the tokens."""
        rule = InPhrases(phrases=[['one']])
        tokens = [Token('one'), Token('two')]
        state = State(token_idx=1)
        match = rule.func(tokens, state)
        self.assertFalse(match)
        self.assertEqual(state, State(token_idx=1))

    def test_func_05(self):
        """Greedy matches the longest rule first."""
        rule = InPhrases(phrases=[['one'], ['one', 'two']])
        tokens = [Token('one'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(match_len=2))

    def test_func_06(self):
        """Lazy matches the shortest rule first."""
        rule = InPhrases(phrases=[['one'], ['one', 'two']], greedy=False)
        tokens = [Token('one'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(match_len=1))

    # def test_func_07(self):
    #     """Greedy match both phrases."""
    #     rule = InPhrases(phrases=[['one'], ['one', 'two']])
    #     tokens = [Token('one'), Token('two'), Token('one')]
    #     state = State()
    #     match = rule.func(tokens, state)
    #     self.assertTrue(match)
    #     self.assertEqual(state, State(match_len=3))
