"""Parse total length notations."""

from pyparsing import Regex, Word, alphas, alphanums
from pyparsing import CaselessLiteral as lit
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class TotalLength(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        words = Word(alphas, alphanums)*(1, 3)

        key_with_units = (
            rx.kwd('totallengthinmillimeters')
            | rx.kwd('totallengthinmm')
            | rx.kwd('total length in millimeters')
            | rx.kwd('total length in mm')
            | rx.kwd('snoutventlengthinmillimeters')
            | rx.kwd('snoutventlengthinmm')
            | rx.kwd('snoutvent length in millimeters')
            | rx.kwd('snoutvent length in mm')
            | rx.kwd('headbodylengthinmillimeters')
            | rx.kwd('headbodylengthinmm')
            | rx.kwd('headbody length in millimeters')
            | rx.kwd('headbody length in mm')
            | rx.kwd('forklengthinmillimeters')
            | rx.kwd('forklengthinmm')
            | rx.kwd('fork length in millimeters')
            | rx.kwd('fork length in mm')
        )

        len_key = Regex(r"""
            total  [\s-]* length [\s-]* in
            | (?: total | max | standard ) [\s-]* lengths?
            | meas [\s*:]? \s* length [\s(]* [l] [)\s:]*
            | meas (?: [a-z]* )? \.? : \s* L
            | t [o.]? l \.? _?
            | s \.? l \.?
            | label [\s.]* lengths?
            | (?: fork | mean | body ) [\s-]* lengths?
            | s \.? v \.? ( l \.? )?
            | snout [\s-]* vent [\s-]* lengths?
            """, rx.flags)

        ambiguous = Regex(r'(?<! [a-z] )(?<! [a-z] \s ) lengths? ', rx.flags)

        key_units_req = (
            lit('measurements') | lit('measurement')
            | lit('body')
            | lit('total')
        )

        parser = (
            key_with_units('units') + rx.pair

            | rx.shorthand_key + rx.pair + rx.len_units('units')
            | rx.shorthand_key + rx.len_units('units') + rx.pair

            | key_units_req + rx.fraction + rx.len_units('units')
            | key_units_req + rx.pair + rx.len_units('units')

            | len_key + rx.fraction + rx.len_units('units')
            | (ambiguous + rx.fraction + rx.len_units('units')
               )('ambiguous_key')

            | rx.pair + rx.len_units('units') + len_key
            | rx.pair + len_key

            | (len_key
               + rx.pair('ft') + rx.feet('ft_units')
               + rx.pair('in') + rx.inches('in_units'))
            | (rx.pair('ft') + rx.feet('ft_units')
               + rx.pair('in') + rx.inches('in_units'))('ambiguous_key')

            # Due to trailing len_key the leading key it is no longer ambiguous
            | ambiguous + rx.pair + rx.len_units('units') + len_key
            | ambiguous + rx.pair + len_key

            | (ambiguous + rx.pair + rx.len_units('units'))('ambiguous_key')
            | (ambiguous + rx.len_units('units') + rx.pair)('ambiguous_key')
            | (ambiguous + rx.pair)('ambiguous_key')

            | rx.shorthand_key + rx.shorthand
            | rx.shorthand

            | len_key + rx.pair + rx.len_units('units')
            | len_key + rx.len_units('units') + rx.pair
            | len_key + rx.pair
            | len_key + words + rx.pair + rx.len_units('units')
            | len_key + words + rx.pair
        )

        parser.ignore(Word(rx.punct, excludeChars=';/'))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_tl') is not None:
            return self.shorthand(match, parts, 'shorthand_tl')
        if parts.get('ft') is not None:
            return self.compound(match, parts)
        if parts.get('numerator') is not None:
            return self.fraction(match, parts)
        return self.simple(match, parts)

    def simple(self, match, parts):
        """Handle a normal length notation."""
        result = Result()
        result.is_flag_in_dict(parts, 'ambiguous_key')
        result.float_value(parts['value1'], parts.get('value2'))
        result.convert_value(parts.get('units'))
        result.ends(match[1], match[2])
        return result

    def compound(self, match, parts):
        """Handle a pattern like: 4 lbs 9 ozs."""
        result = Result()
        result.is_flag_in_dict(parts, 'ambiguous_key')
        result.compound_value(parts, ['ft', 'in'])
        result.ends(match[1], match[2])
        return result

    def fraction(self, match, parts):
        """Handle fractional values like 10 3/8 inches."""
        result = Result()
        result.is_flag_in_dict(parts, 'ambiguous_key')
        result.fraction_value(parts)
        result.convert_value(parts.get('units'))
        result.ends(match[1], match[2])
        return result
