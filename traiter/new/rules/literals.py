"""Look for a sequence of tokens that match the given literals."""

from sys import intern
from .rule import Rule
from ..state import State
from ..token import Tokens


class Literals(Rule):
    """Look for a sequence of tokens that match the given phrases."""

    def __init__(self, **kwargs):
        """Create sets of literals to match against token streams."""
        super().__init__(**kwargs)

        self.lengths = set()
        self.literals = {}  # Key = tuple of words, value = literal index

        literals = kwargs.get('literals', [])
        for i, phrase in enumerate(literals):
            words = []
            for word in phrase:
                words.append(intern(word))
            if not len(words):
                continue
            self.literals[tuple(words)] = i
            self.lengths.add(len(words))

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
        if repeat_count >= self.repeat_lo:
            return True
        state.phrase_len = []
        return False

    def greedy_backtrack(self, state: State) -> bool:
        """Restart the search after where the last one left off."""
        state.phrase_len.pop()
        if len(state.phrase_len) >= self.repeat_lo:
            return True
        return False

    def lazy_backtrack(self, tokens: Tokens, state: State) -> bool:
        """Match token parts against phrase literals."""
        if len(state.phrase_len) == self.repeat_hi:
            state.phrase_len = []
            return False
        return self.repeat(tokens, state)

    def repeat(self, tokens: Tokens, state: State) -> bool:
        """Find the next matching repeat."""
        start = state.token_start + state.total_len

        last = len(self.literals)
        first = last
        phrase_len = 0
        for length in self.lengths:
            end = start + length
            if end > len(tokens):
                continue
            words = [t[self.field] for t in tokens[start:end]]
            phrase = tuple(words)

            position = self.literals.get(phrase, last)
            if position < first:
                first = position
                phrase_len = length

        if phrase_len:
            state.phrase_len.append(phrase_len)
            return True

        return False
