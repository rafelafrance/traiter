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
            key_with_units('units') + rx.range
            | wt_key + rx.mass_units + rx.range
            | wt_key + rx.range + rx.mass_units
            | rx.shorthand_key + rx.range + rx.mass_units
            | rx.shorthand_key + rx.mass_units + rx.range
            | (wt_key
               + rx.range('lbs') + rx.pounds
               + rx.range('ozs') + rx.ounces)
            | (rx.range('lbs') + rx.pounds
               + rx.range('ozs') + rx.ounces
               ).setParseAction(lambda tokens: tokens.append('ambiguous'))
            | wt_key + rx.range
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

        ambiguous = 'ambiguous' in match[0].asList()
        value = self.to_float(parts['value1'])
        value2 = self.to_float(parts['value2'])
        if value2:
            value = [value, value2]
        units = parts.get('units')
        has_units = bool(units)
        value = convert(value, units)

        return Result(value=value, ambiguous=ambiguous, has_units=has_units,
                      start=match[1], end=match[2])

    def shorthand(self, match, parts):
        """Handle shorthand notation like 11-22-33-44:55g."""
        value = self.to_float(parts.get('shorthand_wt'))
        if not value:
            return None
        units = parts.get('shorthand_wt_units')
        has_units = bool(units)
        value = convert(value, units)
        return Result(value=value, has_units=has_units,
                      start=match[1], end=match[2])

    def english(self, match, parts):
        """Handle a pattern like: 4 lbs 9 ozs."""
        ambiguous = 'ambiguous' in match[0].asList()
        value = self.english_value(parts, 'lbs', 'ozs')
        return Result(value=value, ambiguous=ambiguous, has_units=True,
                      start=match[1], end=match[2])
