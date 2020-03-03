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
            rule.literals, {('three', 'four'), ('one', ), ('two', )})

    def test_func_greedy_01(self):
        """It matches a token."""
        rule = Literals(literals=[['one']])
        tokens = [Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(repeat_idx=[1], first_time=False))

    def test_func_greedy_02(self):
        """It matches two tokens."""
        rule = Literals(literals=[['one', 'two']])
        tokens = [Token('one'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(repeat_idx=[2], first_time=False))

    def test_func_greedy_03(self):
        """It matches the second token."""
        rule = Literals(literals=[['two']])
        tokens = [Token('one'), Token('two')]
        state = State(token_idx=1)
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(
            state, State(repeat_idx=[1], token_idx=1, first_time=False))

    def test_func_greedy_04(self):
        """It does not match after the tokens."""
        rule = Literals(literals=[['one']])
        tokens = [Token('one'), Token('two')]
        state = State(token_idx=1)
        match = rule.func(tokens, state)
        self.assertFalse(match)
        self.assertEqual(state, State(token_idx=1, first_time=False))

    def test_func_greedy_05(self):
        """Greedy matches the longest rule first."""
        rule = Literals(literals=[['one'], ['one', 'two']])
        tokens = [Token('one'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(repeat_idx=[2], first_time=False))

    def test_func_greedy_06(self):
        """Greedy match both literals."""
        rule = Literals(repeat_hi=2, literals=[['one'], ['one', 'two']])
        tokens = [Token('one'), Token('two'), Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(repeat_idx=[2, 1], first_time=False))

    def test_func_greedy_07(self):
        """Greedy match repeated literals."""
        rule = Literals(repeat_hi=2, literals=[['one'], ['one', 'one']])
        tokens = [Token('one'), Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(repeat_idx=[2], first_time=False))

    def test_func_greedy_08(self):
        """Greedy minimal match."""
        rule = Literals(repeat_lo=2, repeat_hi=3, literals=[['one']])
        tokens = [Token('one'), Token('two')]
        state = State()
        match = rule.func(tokens, state)
        self.assertFalse(match)
        self.assertEqual(state, State(first_time=False))

    def test_func_greedy_09(self):
        """Greedy maximal match."""
        rule = Literals(repeat_lo=1, repeat_hi=2, literals=[['one']])
        tokens = [Token('one'), Token('one'), Token('one')]
        state = State()
        match = rule.func(tokens, state)
        self.assertTrue(match)
        self.assertEqual(state, State(repeat_idx=[1, 1], first_time=False))

    # def test_func_lazy_01(self):
    #     """Lazy matches the shortest rule first."""
    #     rule = Literals(literals=[['one'], ['one', 'two']], greedy=False)
    #     tokens = [Token('one'), Token('two')]
    #     state = State()
    #     match = rule.func(tokens, state)
    #     self.assertTrue(match)
    #     self.assertEqual(state, State(repeat_idx=[1]))
