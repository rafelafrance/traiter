"""Mix-in for parsing length notations."""

import re
from pylib.numeric_trait import NumericTrait
from pylib.util import FLAGS


LOOK_BACK_FAR = 40

QUOTES_VS_INCHES = re.compile(r' \d " (?! \s* \} )', FLAGS)
IS_COLLECTOR = re.compile(r' collector ', FLAGS)


def add_flags(token, trait):
    """Add common flags to the numeric trait."""
    trait.is_flag_in_token('ambiguous_key', token)
    trait.is_flag_in_token('estimated_value', token)
    # trait.is_value_in_token('measured_from')
    trait.is_value_in_token('measured_from1', token, rename='measured_from')
    trait.is_value_in_token('measured_from2', token, rename='measured_from')
    trait.is_value_in_token('includes', token)


def simple(token):
    """Handle a normal length notation."""
    trait = NumericTrait(start=token.start, end=token.end)
    add_flags(token, trait)
    trait.float_value(token.groups['value1'], token.groups.get('value2'))
    trait.convert_value(token.groups.get('units'))
    return trait


def compound(token, units=''):
    """Handle a pattern like: 4 lbs 9 ozs."""
    trait = NumericTrait(start=token.start, end=token.end)
    add_flags(token, trait)
    values = [token.groups[units[0]], token.groups[units[1]]]
    trait.compound_value(values, units)
    return trait


def fraction(token):
    """Handle fractional values like 10 3/8 inches."""
    trait = NumericTrait(start=token.start, end=token.end)
    add_flags(token, trait)
    trait.fraction_value(token)
    trait.convert_value(token.groups.get('units'))
    return trait


def shorthand_length(token, measurement=''):
    """Handle shorthand length notation like 11-22-33-44:55g."""
    trait = NumericTrait(start=token.start, end=token.end)
    trait.float_value(token.groups.get(measurement))
    if not trait.value:
        return None
    trait.units = 'mm_shorthand'
    trait.units_inferred = False
    trait.is_shorthand = True
    flag = measurement.split('_')[1]
    flag = f'estimated_{flag}'
    trait.is_flag_in_token(flag, token, rename='estimated_value')
    return trait


def numeric_fix_ups(trait, text):
    """All of the numeric fix-ups."""
    return fix_up_shorthand(trait, text) and fix_up_inches(trait, text)


def fix_up_shorthand(trait, text):
    """All of the fix-ups for numbers."""
    if not trait.is_shorthand:
        return trait
    start = max(0, trait.start - LOOK_BACK_FAR)
    if IS_COLLECTOR.search(text, start, trait.start):
        return None
    return trait


def fix_up_inches(trait, text):
    """Disambiguate between double quotes "3" and inch units 3"."""
    if (not trait.units
            and QUOTES_VS_INCHES.match(text[trait.end - 1:])
            and text[trait.start:trait.end].count('"') == 0):
        trait.end += 1
        trait.units = '"'
        trait.convert_value(trait.units)
    return trait
