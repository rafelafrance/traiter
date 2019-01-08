"""Parse total length notations."""

from pyparsing import Regex, Word, alphas, alphanums
# from pyparsing import CaselessLiteral as lit
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class TotalLength(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        words = Word(alphas, alphanums)*(1, 3)

        key_with_units = Regex(r"""
            total  [\s-]* length [\s-]* in [\s-]* (?: mm | millimeters)
            | length [\s-]* in [\s-]* (?: mm | millimeters)
            | snout [\s-]* vent [\s-]* lengths? [\s-]* in [\s-]*
                (?: mm | millimeters)
            | head  [\s-]* body [\s-]* length [\s-]* in [\s-]*
                (?: mm | millimeters)
            """, rx.flags)

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
        key_units_req = Regex(r'measurements? | body | total', rx.flags)

        parser = (
            key_with_units('units') + rx.pair

            | rx.shorthand_key + rx.pair + rx.len_units('units')
            | rx.shorthand_key + rx.len_units('units') + rx.pair

            | key_units_req + rx.fraction + rx.len_units('units')
            | key_units_req + rx.pair + rx.len_units('units')

            | len_key + rx.fraction + rx.len_units('units')
            | (ambiguous + rx.fraction + rx.len_units('units')).setParseAction(
                self.flag_ambiguous_key)

            | rx.pair + rx.len_units('units') + len_key
            | rx.pair + len_key

            | (len_key
               + rx.pair('ft') + rx.feet('ft_units')
               + rx.pair('in') + rx.inches('in_units'))
            | (rx.pair('ft') + rx.feet('ft_units')
               + rx.pair('in') + rx.inches('in_units')).setParseAction(
                   self.flag_ambiguous_key)

            # Due to trailing len_key the leading key it is no longer ambiguous
            | ambiguous + rx.pair + rx.len_units('units') + len_key
            | ambiguous + rx.pair + len_key

            | (ambiguous + rx.pair + rx.len_units('units')).setParseAction(
                self.flag_ambiguous_key)
            | (ambiguous + rx.len_units('units') + rx.pair).setParseAction(
                self.flag_ambiguous_key)
            | (ambiguous + rx.pair).setParseAction(self.flag_ambiguous_key)

            | rx.shorthand_key + rx.shorthand
            | rx.shorthand

            | len_key + rx.pair + rx.len_units('units')
            | len_key + rx.len_units('units') + rx.pair
            | len_key + rx.pair
            | len_key + words + rx.pair + rx.len_units('units')
            | len_key + words + rx.pair
        )

        ignore = Word(rx.punct, excludeChars=';/')
        parser.ignore(ignore)
        return parser

    @staticmethod
    def flag_ambiguous_key(tokens):
        """Flag an ambiguous parse."""
        return tokens.append('ambiguous_key')

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        if parts.get('shorthand_tl') is not None:
            return self.shorthand(match, parts)
        if parts.get('ft') is not None:
            return self.compound(match, parts)
        if parts.get('numerator') is not None:
            return self.fraction(match, parts)
        return self.simple(match, parts)

    def simple(self, match, parts):
        """Handle a normal length notation."""
        result = Result()
        result.is_flag_in_list(match[0].asList(), 'ambiguous_key')
        result.float_value(parts['value1'], parts['value2'])
        result.convert_value(parts.get('units'))
        result.ends(match[1], match[2])
        return result

    def shorthand(self, match, parts):
        """Handle shorthand notation like 11-22-33-44:55g."""
        result = Result()
        result.float_value(parts.get('shorthand_tl'))
        if not result.value:
            return None
        result.units = 'mm_shorthand'
        if parts['shorthand_tl'][-1] == ']':
            result.flags['estimated_value'] = True
        result.ends(match[1], match[2])
        return result

    def compound(self, match, parts):
        """Handle a pattern like: 4 lbs 9 ozs."""
        result = Result()
        result.is_flag_in_list(match[0].asList(), 'ambiguous_key')
        result.compound_value(parts, ['ft', 'in'])
        result.ends(match[1], match[2])
        return result

    def fraction(self, match, parts):
        """Handle fractional values like 10 3/8 inches."""
        result = Result()
        result.is_flag_in_list(match[0].asList(), 'ambiguous_key')
        result.fraction_value(parts)
        result.convert_value(parts.get('units'))
        result.ends(match[1], match[2])
        return result
