"""Tokenize the notations."""

from abc import abstractmethod
from typing import List
from dataclasses import dataclass
import regex
import lib.lexers.shared_regexp as regexp


@dataclass
class Token:
    """What the token is and where we found it in the text."""

    token: str
    start: int = 0
    end: int = 0


Tokens = List[Token]


class LexBase:
    """Shared lexer logic."""

    # Signals the end of a token stream
    sentinel_token = Token(token='-END-', start=0, end=0)

    def __init__(self, lex_rules=None, regex_defines=None):
        """Build the lexer's regexp."""
        self.regexp = ''
        self.lex_rules = self.rule_list()
        self.regex_defines = regexp.DEFINES
        self.build_regex()

    def build_regex(self):
        """Build the lexer's regular expression."""
        regex_defines = regexp.build_regex_defines(self.regex_defines)
        lex_rules = regexp.build_lex_rules(self.lex_rules)

        self.regexp = regex.compile(
            f"""{regex_defines} {lex_rules}""",
            regex.VERBOSE | regex.IGNORECASE)

    @abstractmethod
    def rule_list(self) -> regexp.Regexps:
        """Return the lexer rules for the trait.

        Each trait will have its own list of lexer rules. Note: Order matters.
        """
        return []

    def tokenize(self, text: str) -> Tokens:
        """Split the text into tokens."""
        tokens = []

        for match in self.regexp.finditer(text):
            keys = [k for k, v in match.groupdict().items() if v]
            if keys:
                tokens.append(Token(keys[0], match.start(), match.end()))

        return tokens
