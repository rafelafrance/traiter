"""Parse body mass notations."""

from pyparsing import Regex, Word
from pyparsing import CaselessKeyword as kw
from lib.parsers.base import Base, Result
import lib.parsers.regexp as rx
from lib.parsers.convert_units import convert


class BodyMass(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        key_with_units = kw('weightingrams') | kw('massingrams')

        wt_key = Regex(r"""
            (?: (?: body | full | observed | total ) \s* )?
                (?: weights?
                | weigh (?: s | ed | ing )
                | mass
                | w \.? t s? \.? )
            | body
            """, rx.flags)

        parser = (
            key_with_units('units') + rx.pair
            | wt_key + rx.mass_units + rx.pair
            | wt_key + rx.pair + rx.mass_units
            | rx.shorthand_key + rx.pair + rx.mass_units
            | rx.shorthand_key + rx.mass_units + rx.pair
            | (wt_key
               + rx.pair('lbs') + rx.pounds('lbs_units')
               + rx.pair('ozs') + rx.ounces('ozs_units'))
            | (rx.pair('lbs') + rx.pounds('lbs_units')
               + rx.pair('ozs') + rx.ounces('ozs_units')
               ).setParseAction(lambda tokens: tokens.append('ambiguous_key'))
            | wt_key + rx.pair
            | rx.shorthand_key + rx.shorthand
            | rx.shorthand
        )

        ignore = Word(rx.punct, excludeChars=';')
        parser.ignore(ignore)
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()

        if parts.get('shorthand_tl') is not None:
            return self.shorthand(match, parts)
        if parts.get('lbs') is not None:
            return self.english(match, parts)

        flags = self.ambiguous_key(match)
        value = self.to_float(parts['value1'])
        value2 = self.to_float(parts['value2'])
        if value2:
            value = [value, value2]

        units = parts.get('units')
        if not units:
            flags['units_inferred'] = True
        value = convert(value, units)

        return Result(value=value, flags=flags, units=units,
                      start=match[1], end=match[2])

    def shorthand(self, match, parts):
        """Handle shorthand notation like 11-22-33-44:55g."""
        value = self.to_float(parts.get('shorthand_wt'))
        if not value:
            return None
        units = parts.get('shorthand_wt_units')
        value = convert(value, units)
        flags = {}
        if not units:
            flags['units_inferred'] = True
        if parts.get('shorthand_wt_amb'):
            flags['estimated_value'] = True
        return Result(value=value, units=units, flags=flags,
                      start=match[1], end=match[2])

    def english(self, match, parts):
        """Handle a pattern like: 4 lbs 9 ozs."""
        flags = self.ambiguous_key(match)
        units = [parts['lbs_units'], parts['ozs_units']]
        value = self.english_value(parts, 'lbs', 'ozs')
        return Result(value=value, flags=flags, units=units,
                      start=match[1], end=match[2])
