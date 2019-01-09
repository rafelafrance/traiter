"""Parse body mass notations."""

from pyparsing import Regex, Word
from pyparsing import CaselessLiteral as lit
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class BodyMass(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = rx.kwd('weightingrams') | rx.kwd('massingrams')

        key_leader = lit('body') | lit('full') | lit('observed') | lit('total')
        weight = (
            lit('weights') | lit('weight') | lit('weighs') | lit('weighed')
            | lit('weighing')
        )
        key = (
            key_leader + weight
            | key_leader + rx.lit('mass')
            | weight
            | rx.kwd('mass')
            | rx.kwd('body')
        )

        key_with_dots = Regex(r' \b w \.? t s? \.? ', rx.flags)

        wt_key = key | key_with_dots

        parser = (
            key_with_units('units') + rx.pair
            | wt_key + rx.mass_units('units') + rx.pair
            | wt_key + rx.pair + rx.mass_units('units')
            | rx.shorthand_key + rx.pair + rx.mass_units('units')
            | rx.shorthand_key + rx.mass_units('units') + rx.pair
            | (wt_key
               + rx.number('lbs') + rx.pounds
               + rx.pair('ozs') + rx.ounces)
            | (rx.number('lbs') + rx.pounds + rx.pair('ozs') + rx.ounces
               )('ambiguous_key')
            | wt_key + rx.pair
            | rx.shorthand_key + rx.shorthand
            | rx.shorthand
        )

        parser.ignore(Word(rx.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()

        if parts.get('shorthand_tl') is not None:
            return self.shorthand(match, parts)
        if parts.get('lbs') is not None:
            return self.compound(match, parts)
        return self.simple(match, parts)

    def simple(self, match, parts):
        """Convert a simple value into a result."""
        result = Result()
        result.is_flag_in_dict(parts, 'ambiguous_key')
        result.float_value(parts['value1'], parts['value2'])
        result.convert_value(parts.get('units'))
        result.ends(match[1], match[2])
        return result

    def shorthand(self, match, parts):
        """Convert a shorthand value like 11-22-33-44:55g."""
        result = Result()
        result.float_value(parts.get('shorthand_wt'))
        if not result.value:
            return None
        result.convert_value(parts.get('shorthand_wt_units'))
        result.is_flag_in_dict(parts, 'shorthand_wt_amb', 'estimated_value')
        result.ends(match[1], match[2])
        return result

    def compound(self, match, parts):
        """Convert a compound pattern like: 4 lbs 9 ozs."""
        result = Result()
        result.is_flag_in_dict(parts, 'ambiguous_key')
        result.compound_value(parts, ['lbs', 'ozs'])
        result.ends(match[1], match[2])
        return result
