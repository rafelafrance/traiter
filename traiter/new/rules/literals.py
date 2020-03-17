"""Look for a sequence of tokens that match the given literals."""
from abc import ABC
from sys import intern
from typing import List
from .rule import Rule
from ..state import State
from ..token import Tokens


class Literals(Rule, ABC):  # pylint: disable=abstract-method
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

    def func_greedy(self, tokens: Tokens, state: State) -> bool:
        """Match token parts against phrase literals."""
        if state.first_time:
            return self.greedy_first_time(tokens, state)
        return self.greedy_backtrack(tokens, state)

    def greedy_first_time(self, tokens: Tokens, state: State) -> bool:
        """First time grab as many tokens as possible."""
        state.first_time = False
        token_start = state.token_start
        repeat_count = 0
        while (repeat_count < self.repeat_hi
               and self.next_repeat(tokens, state, token_start)):
            repeat_count += 1
            token_start = state.token_start + state.match_len
        if repeat_count >= self.repeat_lo:
            return True
        state.repeat_idx = []
        return False

    def greedy_backtrack(self, tokens: Tokens, state: State) -> bool:
        """Restart the search after where the last one left off."""
        last_repeat = state.repeat_idx.pop()
        lengths = [i for i in self.lengths if i < last_repeat]
        if self.next_repeat(tokens, state, state.token_start, lengths):
            return True
        if len(state.repeat_idx) < self.repeat_lo:
            state.repeat_idx = []
            return False
        return True

    def func_lazy(self, tokens: Tokens, state: State) -> bool:
        """Match token parts against phrase literals."""

    def next_repeat(self, tokens: Tokens, state: State, token_start: int,
                    lengths: List[int] = None) -> bool:
        """Get the next matching token."""
        if lengths is None:
            lengths = self.lengths

        for length in lengths:
            end = token_start + length
            words = [t[self.field] for t in tokens[token_start:end]]
            if len(words) < length:
                continue
            phrase = tuple(words)
            if phrase in self.literals:
                state.repeat_idx.append(length)
                return True
        return False
