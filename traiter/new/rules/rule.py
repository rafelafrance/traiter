"""Rules for matching tokens."""

from abc import abstractmethod
from typing import List
from ..state import State
from ..token import Tokens


class Rule:
    """How to match tokens."""

    def __init__(self, **kwargs):
        """Create common rule attributes."""
        kwargs = kwargs if kwargs else {}

        # What field to compare in the token
        self.field: str = kwargs.get('field', 'text')

        # Extra data for processing tokens matched by this rule
        self.aux: str = kwargs.get('aux', '')

        # To deal with repeated matches like: + * ? or {3,4}
        self.repeat_lo: int = kwargs.get('repeat_lo', 1)
        self.repeat_hi: int = kwargs.get('repeat_hi', 1)
        self.greedy: bool = kwargs.get('greedy', True)

        if self.repeat_lo > self.repeat_hi:
            self.repeat_lo, self.repeat_hi = self.repeat_hi, self.repeat_lo

    def __eq__(self, other):
        """Compare rules."""
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        """Create string form of the object."""
        return '{}({})'.format(self.__class__.__name__, self.__dict__)

    def func(self, tokens: Tokens, state: State) -> bool:
        """Match token parts against phrase literals."""
        if state.first_time:
            return self.first_time(tokens, state)
        if self.greedy:
            return self.greedy_backtrack(state)
        return self.lazy_backtrack(tokens, state)

    def first_time(self, tokens: Tokens, state: State) -> bool:
        """First time grab as many tokens as possible."""
        state.first_time = False
        repeat_count = 0
        repeat_threshold = self.repeat_hi if self.greedy else self.repeat_lo
        while repeat_count < repeat_threshold and self.repeat(tokens, state):
            repeat_count += 1
        if repeat_count < self.repeat_lo:
            state.phrase_len = []
            return False
        return True

    def greedy_backtrack(self, state: State) -> bool:
        """Restart the search after where the last one left off."""
        state.phrase_len.pop()
        if len(state.phrase_len) < self.repeat_lo:
            state.phrase_len = []
            return False
        return True

    def lazy_backtrack(self, tokens: Tokens, state: State) -> bool:
        """Match token parts against phrase literals."""
        if (len(state.phrase_len) == self.repeat_hi
                or not self.repeat(tokens, state)):
            state.phrase_len = []
            return False
        return True

    @abstractmethod
    def repeat(self, tokens: Tokens, state: State) -> bool:
        """Predicate action."""
        raise NotImplementedError


Pattern = List[Rule]
Patterns = List[Pattern]
