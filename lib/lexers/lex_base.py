"""Tokenize the notations."""

# pylint: disable=too-few-public-methods

from dataclasses import dataclass
from typing import List
import regex
from lib.lexers.util import boundary


@dataclass
class LexRule:
    token: str
    regex: str


@dataclass
class Token:
    token: str
    start: int = 0
    end: int = 0


Tokens = List[Token]


class LexBase:
    """Shared lexer logic."""

    def __init__(self):
        """Build the regex."""
        joined = ' | '.join(
            [f' (?P<{r.token}> {r.regex} ) ' for r in self.tokens])
        self.regex = regex.compile(joined, regex.VERBOSE | regex.IGNORECASE)

    def tokenize(self, raw: str) -> Tokens:
        """Split the text into tokens."""
        tokens = []

        for match in self.regex.finditer(raw):
            keys = [k for k, v in match.groupdict().items() if v]
            if keys:
                tokens.append(Token(keys[0], match.start(), match.end()))

        return tokens

    # #########################################################################
    # Token regexes used by more than one lexer

    # Numbers are positive & decimals
    number = LexRule(
        'number', r' (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? ')

    # Used to parse numeric ranges
    to = LexRule('to', r' - | to ')

    # Used to parse length x width values
    cross = LexRule('cross', r'  x | by | \* ')

    word = LexRule('word', boundary(r' \w+ '))   # Generic word

    # Used to separate key1=value1; key2=val2 pairs
    stop = LexRule('stop', r' [.;] ')

    # Order matters!
    tokens = [number, to, cross, word, stop]

    sentinel_token = Token(token='END', start=0, end=0)
