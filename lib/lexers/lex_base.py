"""Tokenize the notations."""

# pylint: disable=too-few-public-methods,missing-docstring

from abc import abstractmethod
from typing import List
from dataclasses import dataclass
import regex


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
LexRules = List[LexRule]


class LexBase:
    """Shared lexer logic."""

    # #########################################################################
    # Signals the end of a token stream

    sentinel_token = Token(token='END', start=0, end=0)

    # #########################################################################

    def __init__(self):
        """Build the regex."""
        self.tokens = self.rule_list()
        joined = ' | '.join(
            [f' (?P<{r.token}> {r.regex} ) ' for r in self.tokens])
        self.regex = regex.compile(joined, regex.VERBOSE | regex.IGNORECASE)

    @abstractmethod
    def rule_list(self) -> LexRules:
        """Return the lexer rules for the trait.

        Note: Order matters.
        """
        return [self.number, self.to, self.cross, self.word, self.stop]

    # #########################################################################
    # Common regex fragments used in more than one lexer

    # Numbers are positive & decimals
    @property
    def re_number(self):
        return r' (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? '

    # #########################################################################
    # Tokens used by more than one lexer

    @property
    def number(self):
        return LexRule(
            'number', self.re_number)

    # Used to parse numeric ranges
    @property
    def to(self):
        return LexRule('to', r' - | to ')

    # Used to parse length x width values
    @property
    def cross(self):
        return LexRule('cross', r'  x | by | \* ')

    @property
    def word(self):
        return LexRule('word', self.boundary(r' \w+ '))   # Generic word

    # Used to separate key1=value1; key2=val2 pairs
    @property
    def stop(self):
        return LexRule('stop', r' [.;] ')

    # #########################################################################

    def tokenize(self, raw: str) -> Tokens:
        """Split the text into tokens."""
        tokens = []

        for match in self.regex.finditer(raw):
            keys = [k for k, v in match.groupdict().items() if v]
            if keys:
                tokens.append(Token(keys[0], match.start(), match.end()))

        return tokens

    @staticmethod
    def boundary(regex):
        r"""Wrap a regular expression in \b character class.

        This is used to "delimit" a word on a word boundary so the regex does
        not match the interior of a word.

        - This is helpful for keyword searches like 't'. Without this 't' would
          match both 't's in 'that' but the regex in \b neither 't' is matched.
          Only 't's like ' t ', or '$t.', etc. will match.
        - It is not helpful for searching for things like '19mm' where there is
          no word break between the two tokens.
        - It is also not helpful if your pattern ends or starts with a non-word
          character.
        """
        return r'\b (?: {} ) \b'.format(regex)
