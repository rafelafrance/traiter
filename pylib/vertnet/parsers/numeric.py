"""Utilities for parsing numeric traits."""

import regex
from pylib.shared.util import to_float, squash, as_list
from pylib.vertnet.trait import Trait
from pylib.vertnet.util import FLAGS
from pylib.vertnet.convert_units import convert


LOOK_BACK_FAR = 40

QUOTES_VS_INCHES = regex.compile(r' \d " (?! \s* \} )', FLAGS)
IS_COLLECTOR = regex.compile(r' collector ', FLAGS)


def as_value(token, trait, value='number', units='units'):
    """Convert token values and units to trait fields."""
    trait.units = token.groups.get(units)
    values = []
    for val in as_list(token.groups.get(value, [])):
        val = to_float(val)
        if val is None:
            return False
        values.append(convert(val, trait.units))
    trait.value = squash(values)
    trait.units_inferred = not bool(trait.units)
    return True


def add_flags(token, trait):
    """Add common flags to the numeric trait."""
    trait.is_flag_in_token('ambiguous_key', token)
    trait.is_flag_in_token('estimated_value', token)
    trait.is_value_in_token('measured_from1', token, rename='measured_from')
    trait.is_value_in_token('measured_from2', token, rename='measured_from')
    trait.is_value_in_token('includes', token)
    trait.is_flag_in_token('quest', token, rename='uncertain')
    # trait.is_flag_missing('key', token, rename='ambiguous_key')


def simple(token, value='number', units='units'):
    """Handle a normal length notation."""
    trait = Trait(start=token.start, end=token.end)
    flag = as_value(token, trait, value, units)
    add_flags(token, trait)
    return trait if flag else None


def compound(token, units=''):
    """Handle a pattern like: 4 lbs 9 ozs."""
    trait = Trait(start=token.start, end=token.end)
    add_flags(token, trait)
    values = [token.groups[units[0]], token.groups[units[1]]]
    trait.compound_value(values, units)
    return trait


def fraction(token):
    """Handle fractional values like 10 3/8 inches."""
    trait = Trait(start=token.start, end=token.end)
    trait.units = token.groups.get('units')
    whole = to_float(token.groups.get('whole', '0'))
    numerator = to_float(token.groups['numerator'])
    denominator = to_float(token.groups['denominator'])
    trait.value = whole + numerator / denominator
    if trait.units:
        trait.value = convert(trait.value, trait.units)
    add_flags(token, trait)
    return trait


def shorthand_length(token, measurement=''):
    """Handle shorthand length notation like 11-22-33-44:55g."""
    trait = Trait(start=token.start, end=token.end)
    trait.value = to_float(token.groups.get(measurement))
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
        trait.units_inferred = False
        trait.value = convert(trait.value, trait.units)
    return trait
