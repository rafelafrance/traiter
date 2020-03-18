"""Test literal matches."""

import unittest
from traiter.new.rules.literals import Literals
from traiter.new.token import Token
from traiter.new.state import State


class TestLiterals(unittest.TestCase):
    """Test literal matches."""

    def test__init__01(self):
        """It builds literals."""
        rule = Literals(literals=[['one'], ['two'], ['three', 'four']])
        self.assertEqual(
            rule.literals, {('one', ): 0, ('two', ): 1, ('three', 'four'): 2})

    def test_greedy_first_time_01(self):
        """It matches a token."""
        rule = Literals(literals=[['one']])
        tokens = [Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[1], first_time=False))

    def test_greedy_first_time_02(self):
        """It matches two tokens."""
        rule = Literals(literals=[['one', 'two']])
        tokens = [Token('one'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[2], first_time=False))

    def test_greedy_first_time_03(self):
        """It matches the second token."""
        rule = Literals(literals=[['two']])
        tokens = [Token('one'), Token('two')]
        state = State(token_start=1)
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(
            state, State(phrase_len=[1], token_start=1, first_time=False))

    def test_greedy_first_time_04(self):
        """It does not match after the tokens."""
        rule = Literals(literals=[['one']])
        tokens = [Token('one'), Token('two')]
        state = State(token_start=1)
        match = rule.func(tokens, state)
        self.assertFalse(match)
        self.assertEqual(state, State(token_start=1, first_time=False))

    def test_greedy_first_time_05(self):
        """Greedy matches both literals."""
        rule = Literals(repeat_hi=2, literals=[['one', 'two'], ['one']])
        tokens = [Token('one'), Token('two'), Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[2, 1], first_time=False))

    def test_greedy_first_time_06(self):
        """Greedy match repeated literals."""
        rule = Literals(repeat_hi=2, literals=[['one']])
        tokens = [Token('one'), Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[1, 1], first_time=False))

    def test_greedy_first_time_07(self):
        """Greedy minimal match."""
        rule = Literals(repeat_lo=2, repeat_hi=3, literals=[['one']])
        tokens = [Token('one'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertFalse(match)
        self.assertEqual(state, State(first_time=False))

    def test_greedy_first_time_08(self):
        """Greedy maximal match."""
        rule = Literals(repeat_lo=1, repeat_hi=2, literals=[['one']])
        tokens = [Token('one'), Token('one'), Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[1, 1], first_time=False))

    def test_greedy_first_time_09(self):
        """Greedy zero length match."""
        rule = Literals(repeat_lo=0, repeat_hi=2, literals=[['one']])
        tokens = [Token('two'), Token('two'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[], first_time=False))

    def test_greedy_backtrack_01(self):
        """Backtrack shrinks the match."""
        rule = Literals(repeat_lo=1, repeat_hi=2, literals=[['one']])
        tokens = [Token('one'), Token('one')]
        state = State()
        rule.func(tokens, state)
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[1], first_time=False))

    def test_lazy_first_time_01(self):
        """It matches a token."""
        rule = Literals(literals=[['one']], greedy=False)
        tokens = [Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[1], first_time=False))

    def test_lazy_first_time_02(self):
        """It matches two tokens."""
        rule = Literals(literals=[['one', 'two']], greedy=False)
        tokens = [Token('one'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[2], first_time=False))

    def test_lazy_first_time_03(self):
        """It matches the second token."""
        rule = Literals(literals=[['two']], greedy=False)
        tokens = [Token('one'), Token('two')]
        state = State(token_start=1)
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(
            state, State(phrase_len=[1], token_start=1, first_time=False))

    def test_lazy_first_time_04(self):
        """It does not match after the tokens."""
        rule = Literals(literals=[['one']], greedy=False)
        tokens = [Token('one'), Token('two')]
        state = State(token_start=1)
        match = rule.func(tokens, state)
        self.assertFalse(match)
        self.assertEqual(state, State(token_start=1, first_time=False))

    def test_lazy_first_time_05(self):
        """Lazy matches only the first literals."""
        rule = Literals(
            repeat_hi=2, literals=[['one', 'two'], ['one']], greedy=False)
        tokens = [Token('one'), Token('two'), Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[2], first_time=False))

    def test_lazy_first_time_06(self):
        """Lazy minimal match."""
        rule = Literals(
            repeat_lo=2, repeat_hi=3, literals=[['one']], greedy=False)
        tokens = [Token('one'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertFalse(match)
        self.assertEqual(state, State(first_time=False))

    def test_lazy_first_time_07(self):
        """Lazy minimal match."""
        rule = Literals(
            repeat_lo=2, repeat_hi=3, literals=[['one']], greedy=False)
        tokens = [Token('one'), Token('one'), Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[1, 1], first_time=False))

    def test_lazy_first_time_08(self):
        """Lazy zero length match."""
        rule = Literals(
            repeat_lo=0, repeat_hi=2, literals=[['one']], greedy=False)
        tokens = [Token('two'), Token('two'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[], first_time=False))

    def test_lazy_backtrack_01(self):
        """Lazy backtrack expands the match."""
        rule = Literals(
            repeat_lo=2, repeat_hi=3, literals=[['one']], greedy=False)
        tokens = [Token('one'), Token('one'), Token('one')]
        state = State()
        rule.func(tokens, state)
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(phrase_len=[1, 1, 1], first_time=False))

    def test_lazy_backtrack_02(self):
        """Lazy backtrack expands fails when repeat is too big."""
        rule = Literals(
            repeat_lo=2, repeat_hi=2, literals=[['one']], greedy=False)
        tokens = [Token('one'), Token('one'), Token('one')]
        state = State()
        rule.func(tokens, state)
        match = rule.func(tokens, state)
        self.assertFalse(match)
        self.assertEqual(state, State(phrase_len=[], first_time=False))
