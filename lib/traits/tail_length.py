"""Parse tail length notations."""

from pyparsing import Word
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class TailLength(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = (
            rx.kwd('taillengthinmillimeters')
            | rx.kwd('taillengthinmm')
            | rx.kwd('tail length in millimeters')
            | rx.kwd('tail length in mm')
        )

        key = (
            rx.kwd('tail length')
            | rx.kwd('tail len')
            | rx.kwd('taillength')
            | rx.kwd('taillen')
            | rx.kwd('tail')
            | rx.kwd('tal')
        )

        parser = (
            key_with_units('units') + rx.pair
            | key + rx.pair + rx.len_units('units')
            | key + rx.pair
            | rx.shorthand_key + rx.shorthand
            | rx.shorthand
        )

        parser.ignore(Word(rx.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_tal') is not None:
            return self.shorthand(match, parts, 'shorthand_tal')
        return self.simple(match, parts)

    def simple(self, match, parts):
        """Convert parsed tokens into a result."""
        result = Result()
        result.float_value(parts['value1'], parts['value2'])
        result.convert_value(parts.get('units'))
        result.ends(match[1], match[2])
        return result
