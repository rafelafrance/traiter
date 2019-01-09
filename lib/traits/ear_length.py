"""Parse ear length notations."""

# from pyparsing import Word
from lib.base import Base
from lib.result import Result
# import lib.regexp as rx


class EarLength(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        # parser.ignore(Word(rx.punct))
        # return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_el') is not None:
            return self.shorthand(match, parts, 'shorthand_el')
        return self.simple(match, parts)

    def simple(self, match, parts):
        """Convert parsed tokens into a result."""
        result = Result()
        result.float_value(parts['value1'], parts['value2'])
        result.convert_value(parts.get('units'))
        result.ends(match[1], match[2])
        return result
