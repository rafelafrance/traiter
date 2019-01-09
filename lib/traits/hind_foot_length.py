"""Parse hind foot length notations."""

# from pyparsing import Word
from lib.base import Base
from lib.numeric import Numeric
# import lib.regexp as rx


class HindFootLength(Base, Numeric):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        # parser.ignore(Word(rx.punct))
        # return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_hfl') is not None:
            return self.shorthand_length(match, parts, 'shorthand_hfl')
        return self.simple(match, parts)
