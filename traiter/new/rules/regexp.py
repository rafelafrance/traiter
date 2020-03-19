"""Look for a sequence of tokens that match the given regular expression."""

import regex  # type: ignore
from .rule import Rule
from ..state import State
from ..token import Tokens


class Regexp(Rule):
    """Look for a sequence of tokens that match the given regex."""

    def __init__(self, **kwargs):
        """Create a regex to match against token streams."""
        super().__init__(**kwargs)

        flags = kwargs.get('flags', regex.IGNORECASE | regex.VERBOSE)
        self.regexp = regex.compile(kwargs['regexp'], flags=flags)

    def repeat(self, tokens: Tokens, state: State) -> bool:
        """Find the next token that matches the regex."""
        match = self.regexp.search(tokens[state.token_start][self.field])
        if match:
            state.phrase_len.append(1)
            return True
        return False
