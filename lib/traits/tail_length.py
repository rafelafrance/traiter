"""Parse tail length notations."""

from pyparsing import Word
# from pyparsing import CaselessLiteral as lit
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class TailLength(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = (
            rx.kwd('taillengthinmm')
            | rx.kwd('taillengthinmillimeters')
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

        ignore = Word(rx.punct)
        parser.ignore(ignore)
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_tl') is not None:
            return self.shorthand(match, parts)
        return self.simple(match, parts)

    def simple(self, match, parts):
        """Convert parsed tokens into a result."""
        result = Result()
        result.is_flag_in_list(match[0].asList(), 'ambiguous_key')
        result.float_value(parts['value1'], parts['value2'])
        result.convert_value(parts.get('units'))
        result.ends(match[1], match[2])
        return result

    def shorthand(self, match, parts):
        """Handle shorthand notation like 11-22-33-44:55g."""
        result = Result()
        result.float_value(parts.get('shorthand_tal'))
        if not result.value:
            return None
        result.units = 'mm_shorthand'
        if parts['shorthand_tal'][-1] == ']':
            result.flags['estimated_value'] = True
        result.ends(match[1], match[2])
        return result
