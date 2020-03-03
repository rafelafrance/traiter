"""Look for a sequence of tokens that match the given literals."""

from sys import intern
from .rule import Rule
from ..state import State
from ..token import Tokens


class Literals(Rule):  # pylint: disable=abstract-method
    """Look for a sequence of tokens that match the given phrases."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        lengths = set()
        self.literals = set()

        literals = kwargs.get('literals', [])
        for phrase in literals:
            words = []
            for word in phrase:
                words.append(intern(word))
            self.literals.add(tuple(words))
            lengths.add(len(words))

        self.lengths = sorted(list(lengths), reverse=self.greedy)
        self.func = self.func_greedy if self.greedy else self.func_lazy

    def next_repeat(self, tokens: Tokens, state: State, start: int) -> bool:
        """Get the next matching token."""
        for length in self.lengths:
            end = start + length
            words = [t[self.field] for t in tokens[start:end]]
            if len(words) < length:
                continue
            phrase = tuple(words)
            if phrase in self.literals:
                state.repeat_idx.append(length)
                return True
        return False

    def func_greedy(self, tokens: Tokens, state: State) -> bool:
        """Match token parts against phrase literals."""
        # First time gobble up as much as we can
        if state.first_time:
            return self.greedy_first_time(tokens, state)

        # For next match backtrack and try again
        else:
            pass

        return False

    def greedy_first_time(self, tokens: Tokens, state: State) -> bool:
        """First time grab as many tokens as possible."""
        state.first_time = False
        start = state.token_idx
        repeat_count = 0
        while (repeat_count < self.repeat_hi
               and self.next_repeat(tokens, state, start)):
            repeat_count += 1
            start = state.token_idx + state.match_len
        if repeat_count >= self.repeat_lo:
            return True
        state.repeat_idx = []
        return False

    def func_lazy(self, tokens: Tokens, state: State) -> bool:
        """Match token parts against phrase literals."""
