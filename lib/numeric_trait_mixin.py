"""Mix-in for parsing length notations."""

import re
from lib.parsed_trait import ParsedTrait


class NumericTraitMixIn:
    """Shared parser logic."""

    @staticmethod
    def simple(match, parts):
        """Handle a normal length notation."""
        result = ParsedTrait()
        result.is_flag_in_dict(parts, 'ambiguous_key')
        result.float_value(parts['value1'], parts.get('value2'))
        result.convert_value(parts.get('units'))
        result.ends(match[1], match[2])
        return result

    @staticmethod
    def shorthand_length(match, parts, key):
        """Handle shorthand length notation like 11-22-33-44:55g."""
        result = ParsedTrait()
        result.float_value(parts.get(key))
        if not result.value:
            return None
        result.units = 'mm_shorthand'
        if parts[key][-1] == ']':
            result.flags['estimated_value'] = True
        result.ends(match[1], match[2])
        return result

    @staticmethod
    def compound(match, parts, units):
        """Handle a pattern like: 4 lbs 9 ozs."""
        result = ParsedTrait()
        result.is_flag_in_dict(parts, 'ambiguous_key')
        result.compound_value(parts, units)
        result.ends(match[1], match[2])
        return result

    @staticmethod
    def fraction(match, parts):
        """Handle fractional values like 10 3/8 inches."""
        result = ParsedTrait()
        result.is_flag_in_dict(parts, 'ambiguous_key')
        result.fraction_value(parts)
        result.convert_value(parts.get('units'))
        result.ends(match[1], match[2])
        return result

    @staticmethod
    def fix_up_inches(text, result):
        """Disambiguate between double quotes "1" & inch units 3"."""
        if (not result.units
                and text[result.end-1].isdigit()
                and result.end < len(text)
                and text[result.start:result.end].count('"') == 0
                and re.match(r'"(?!\s*\})', text[result.end:])):

            result.end += 1
            result.units = '"'
            result.convert_value(result.units)

        return result
