"""Mix-in for parsing length notations."""

import re
from lib.trait import Trait


QUOTES_VS_INCHES = re.compile(r' \d " (?! \s* \} )', re.VERBOSE)


class NumericParserMixIn:
    """Shared parser logic."""

    @staticmethod
    def simple(token):
        """Handle a normal length notation."""
        trait = Trait(start=token.start, end=token.end)
        trait.is_flag_in_token('ambiguous_key', token)
        trait.is_flag_in_token('ambiguous_char', token)
        trait.is_flag_in_token('estimated_value', token)
        trait.flag_from_token('measured_from', token)
        trait.float_value(token.groups['value1'], token.groups.get('value2'))
        trait.convert_value(token.groups.get('units'))
        return trait

    @staticmethod
    def shorthand_length(token, measurement=None):
        """Handle shorthand length notation like 11-22-33-44:55g."""
        trait = Trait(start=token.start, end=token.end)
        trait.float_value(token.groups.get(measurement))
        if not trait.value:
            return None
        trait.units = 'mm_shorthand'
        flag = measurement.split('_')[1]
        flag = f'estimated_{flag}'
        trait.is_flag_in_token(flag, token, rename='estimated_value')
        return trait

    @staticmethod
    def compound(token, units=None):
        """Handle a pattern like: 4 lbs 9 ozs."""
        trait = Trait(start=token.start, end=token.end)
        trait.is_flag_in_token('ambiguous_key', token)
        values = [token.groups[units[0]], token.groups[units[1]]]
        trait.compound_value(values, units)
        return trait

    @staticmethod
    def fraction(token):
        """Handle fractional values like 10 3/8 inches."""
        trait = Trait(start=token.start, end=token.end)
        trait.is_flag_in_token('ambiguous_key', token)
        trait.fraction_value(token)
        trait.convert_value(token.groups.get('units'))
        return trait

    @staticmethod
    def fix_up_inches(trait, text):
        """Disambiguate between double quotes "3" and inch units 3"."""
        if (not trait.units
                and QUOTES_VS_INCHES.match(text[trait.end-1:])
                and text[trait.start:trait.end].count('"') == 0):
            trait.end += 1
            trait.units = '"'
            trait.convert_value(trait.units)
        return trait
