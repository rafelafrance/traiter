"""Look for a sequence of tokens that match the given phrases."""

from sys import intern
from collections import defaultdict
from .rule import Rule
from ..state import State
from ..token import Tokens


class InPhrases(Rule):
    """Look for a sequence of tokens that match the given phrases."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pdict = defaultdict(set)  # key = length, value = phrase set
        phrases = kwargs['phrases'] if kwargs.get('phrases') else []
        for phrase in phrases:
            plist = []
            for word in phrase:
                plist.append(intern(word))
            pdict[len(plist)].add(tuple(plist))

        self.values = [(k, pdict[k]) for k
                       in sorted(pdict.keys(), reverse=self.greedy)]

    def func(self, tokens: Tokens, state: State) -> bool:
        """Match token parts against phrase literals."""
        v = state.value_idx
        for phrases in self.values[v:]:
            start = state.token_idx
            end = start + phrases[0]
            words = [t[self.field] for t in tokens[start:end]]
            phrase = tuple(words)
            if phrase in phrases[1]:
                state.value_idx = v
                state.match_len = phrases[0]
                return True
            v += 1
        return False
