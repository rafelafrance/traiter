"""Test regexp matches."""

import unittest
from traiter.new.rules.regexp import Regexp
from traiter.new.token import Token
from traiter.new.state import State


class TestMatch(unittest.TestCase):
    """Test literal matches."""

    def test_first_time_01(self):
        """It matches a token."""
        rule = Regexp(regexp=r'one')
        tokens = [Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[1], first_time=False))

    def test_first_time_02(self):
        """It matches the second token."""
        rule = Regexp(regexp=r'two')
        tokens = [Token('one'), Token('two')]
        state = State(token_start=1)
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(
            state, State(phrase_len=[1], token_start=1, first_time=False))

    def test_first_time_03(self):
        """It matches the maximum of tokens."""
        rule = Regexp(regexp=r'one', repeat_hi=3)
        tokens = [Token('one'), Token('one'), Token('one'), Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(
            state, State(phrase_len=[1, 1, 1], first_time=False))

    def test_first_time_04(self):
        """It lazy matches tokens."""
        rule = Regexp(regexp=r'one', repeat_hi=3, greedy=False)
        tokens = [Token('one'), Token('one'), Token('one'), Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(
            state, State(phrase_len=[1], first_time=False))
