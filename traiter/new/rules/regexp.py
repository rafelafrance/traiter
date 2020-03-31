"""Look for a sequence of tokens that match the given regular expression."""

import regex  # type: ignore
from ..state import State
from ..token import Tokens, field
from .rule import Rule


class Regexp(Rule):
    """Look for a sequence of tokens that match the given regex."""

    def __init__(self, **kwargs):
        """Create a regex to match against token streams."""
        super().__init__(**kwargs)

        flags = kwargs.get('flags', regex.IGNORECASE | regex.VERBOSE)
        self.regexp = regex.compile(kwargs['regexp'], flags=flags)

    def repeat(self, doc: Tokens, state: State) -> bool:
        """Find the next token that matches the regex."""
        token = doc[state.token_start]
        text = field(token, self.field)
        match = self.regexp.search(text)
        if match:
            state.phrase_len.append(1)
            return True
        return False
