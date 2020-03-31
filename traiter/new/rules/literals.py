"""Look for a sequence of tokens that match the given literals."""

from sys import intern
from ..state import State
from ..token import Tokens, field
from .rule import Rule


class Literals(Rule):
    """Look for a sequence of tokens that match the given phrases."""

    def __init__(self, **kwargs):
        """Create a set of literals to match against token streams."""
        super().__init__(**kwargs)

        self.lengths = set()
        self.literals = {}  # Key = tuple of words, value = literal index

        literals = kwargs.get('literals', [])
        for i, phrase in enumerate(literals):
            words = []
            for word in phrase:
                words.append(intern(word))
            if len(words) == 0:
                continue
            self.literals[tuple(words)] = i
            self.lengths.add(len(words))

    def repeat(self, doc: Tokens, state: State) -> bool:
        """Find the next matching repeat."""
        start = state.token_start + state.total_len

        last = len(self.literals)
        first = last
        phrase_len = 0
        for length in self.lengths:
            end = start + length
            if end > len(doc):
                continue
            words = [field(t, self.field) for t in doc[start:end]]
            phrase = tuple(words)

            position = self.literals.get(phrase, last)
            if position < first:
                first = position
                phrase_len = length

        if phrase_len:
            state.phrase_len.append(phrase_len)
            return True

        return False
