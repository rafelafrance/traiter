"""Tokenize the notations."""

# pylint: disable=too-few-public-methods,missing-docstring

from abc import abstractmethod
from typing import List
from dataclasses import dataclass
import regex
import lib.lexers.shared_lex_rules as rule
import lib.lexers.shared_regex_defines as define


@dataclass
class Token:
    token: str
    start: int = 0
    end: int = 0


Tokens = List[Token]


class LexBase:
    """Shared lexer logic."""

    # #########################################################################
    # Signals the end of a token stream

    sentinel_token = Token(token='-END-', start=0, end=0)

    # #########################################################################

    def __init__(self, lex_rules=None, regex_defines=None):
        """Build the lexer's regex."""
        self._lex_rules = lex_rules
        if lex_rules is None:
            self._lex_rules = self.rule_list()

        self._regex_defines = regex_defines
        if regex_defines is None:
            self._regex_defines = [define.decimal, define.metric_wt]

        self.regex = self.build_regex()

    @property
    def lex_rules(self):
        return self._lex_rules

    @lex_rules.setter
    def lex_rules(self, lex_rules: rule.LexRules):
        self._lex_rules += lex_rules
        self.regex = self.build_regex()

    @lex_rules.deleter
    def lex_rules(self):
        self._lex_rules = []
        self.regex = self.build_regex()

    @property
    def regex_defines(self):
        return self._regex_defines

    @regex_defines.setter
    def regex_defines(self, regex_defines: define.Defines):
        self._regex_defines += regex_defines
        self.regex = self.build_regex()

    @regex_defines.deleter
    def regex_defines(self):
        self._regex_defines = []
        self.regex = self.build_regex()

    def build_regex(self):
        regex_defines = define.build_regex_defines(self.regex_defines)
        lex_rules = rule.build_lex_rules(self.lex_rules)

        return regex.compile(
            f"""(?(DEFINE) {regex_defines} ) {lex_rules}""",
            regex.VERBOSE | regex.IGNORECASE)

    # #########################################################################

    @abstractmethod
    def rule_list(self) -> rule.LexRules:
        """Return the lexer rules for the trait.

        Each trait will have its own list of lexer rules. Note: Order matters.
        """
        return []

    # #########################################################################

    def tokenize(self, raw: str) -> Tokens:
        """Split the text into tokens."""
        tokens = []

        for match in self.regex.finditer(raw):
            keys = [k for k, v in match.groupdict().items() if v]
            if keys:
                tokens.append(Token(keys[0], match.start(), match.end()))

        return tokens
