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


LexRules = List[LexRule]


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

    sentinel_token = Token(token='END', start=0, end=0)

    # #########################################################################

    def __init__(self):
        """Build the regex."""
        self.tokens = self.rule_list()

        joined = ' | '.join(
            [f' (?P<{r.token}> {r.regex} ) ' for r in self.tokens])

        defines = ' '.join(self.defines())

        self.regex = regex.compile(
            f"""(?(DEFINE) {defines} ) {joined}""",
            regex.VERBOSE | regex.IGNORECASE)

    @abstractmethod
    def rule_list(self) -> LexRules:
        """Return the lexer rules for the trait.

        Note: Order matters.
        """
        # Returning this list only for testing. Overridden elsewhere
        return [self.number, self.to, self.cross, self.word, self.stop]

    def defines(self):
        """ These DEFINEs will appear in the lexer's regexs."""
        return [self.define_decimal]

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
    def boundary(regex, left=True, right=True):
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
        left = r'\b' if left else ''
        right = r'\b' if right else ''
        return r'{} (?: {} ) {}'.format(left, regex, right)

    # #########################################################################
    # Common regex fragments used in more than one lexer

    # Numbers are positive decimals
    @property
    def define_decimal(self):
        return r"""(?P<decimal>
            (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? )"""

    # #########################################################################
    # Tokens used by more than one lexer

    @property
    def number(self):
        return LexRule('number', ' (?&decimal) ')

    @property
    def fraction(self):
        return LexRule('fraction', r' (?: \d+ \s+ )? \d+ / \d+ ')

    @property
    def range(self):
        return LexRule(
            'range', r' (?&decimal) (?: \s* (?: - | to ) \s* (?&decimal) )? ')

    @property
    def to(self):
        return LexRule('to', r' - | to ')

    # Used to parse length x width values
    @property
    def cross(self):
        return LexRule('cross', r'  x | by | \* ')

    @property
    def shorthand_key(self):
        return LexRule('shorthand_key', self.boundary(r"""
            on \s* tag | specimens? | catalog
            | meas(?: urements )? [:.,]? (?: \s* length \s* )?
                (?: \s+ \(? [\p{Letter}]+ \)? \.? ){0,2}
            | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
            | mesurements | Measurementsnt
        """))

    @property
    def shorthand(self):
        return LexRule('shorthand', r"""
            (?<! [:-] )            # Handle list notation
            (?: (?&decimal) | [?x] )
            (?: [:-] (?: (?&decimal) | [?x]{1,2}) ){2,3}
            (?: (?: [=:-] | \s+ ) (?: (?&decimal) | [?x]{1,2})? )
            (?! [\s:/-] )          # Handle list notation
        """)

    @property
    def word(self):
        return LexRule('word', self.boundary(r' \w+ '))   # Generic word

    # Used to separate key1=value1; key2=val2 pairs
    @property
    def stop(self):
        return LexRule('stop', r' [.;] ')

    @property
    def feet(self):
        return LexRule('feet', r' (?: foot | feet | ft ) s? \.? ')

    @property
    def inches(self):
        return LexRule('inches', r' (?: inch e? | in ) s? \.? ')

    @property
    def metric_len(self):
        return LexRule('metric_len', r"""
            (?: [cm] [\s.]? m ) | meters? | millimeters? | centimeters?
        """)
