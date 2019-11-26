"""Functions common to most male & female reproductive traits."""

from string import punctuation
from copy import copy
from pylib.vertnet.numeric import as_value
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import fragment
from pylib.vertnet.shared_patterns import RULE
from pylib.vertnet.trait import Trait


# Used to get compounds traits from a single parse
DOUBLE_CROSS = fragment(
    name='double_cross', regexp=f' {RULE["cross"].pattern} ')

SIDES = {
    'l': 'r', 'r': 'l',
    'left': 'right', 'right': 'left',
    'lft': 'rt', 'rt': 'lft'}


def double(token):
    """Convert a single token into multiple (two) parsers."""
    trait1 = Trait(start=token.start, end=token.end)
    token1 = Token(DOUBLE_CROSS, groups=copy(token.groups))
    token1.groups['units'] = token.groups.get('units_1')
    token1.groups['value'] = token.groups.get('value_1')
    side1 = token.groups.get('side_1')

    trait2 = Trait(start=token.start, end=token.end)
    token2 = Token(DOUBLE_CROSS, groups=copy(token.groups))
    token2.groups['units'] = token.groups.get('units_2')
    token2.groups['value'] = token.groups.get('value_2')
    side2 = token.groups.get('side_2')

    if token1.groups['units'] and not token2.groups['units']:
        token2.groups['units'] = token1.groups['units']
    elif token2.groups['units'] and not token1.groups['units']:
        token1.groups['units'] = token2.groups['units']

    flag1 = as_value(token1, trait1, value_field='value')
    flag2 = as_value(token2, trait2, value_field='value')
    if not flag1 or not flag2:
        return None

    side1 = side1.lower().strip(punctuation) if side1 else None
    side2 = side2.lower().strip(punctuation) if side2 else None
    side1 = SIDES.get(side2) if not side1 else side1
    side2 = SIDES.get(side1) if not side2 else side2

    if side1:
        trait1.side = side1
    if side2:
        trait2.side = side2

    return [trait1, trait2]


def convert(token):
    """Convert parsed token into a trait product."""
    trait = Trait(start=token.start, end=token.end)
    flag = as_value(token, trait, unit_field='len_units')

    trait.is_flag_in_token('ambiguous_char', token, rename='ambiguous_key')
    trait.is_flag_in_token('ambiguous_key', token)
    trait.is_value_in_token('dimension', token)
    trait.is_value_in_token('dim', token, rename='dimension')
    trait.is_value_in_token('side', token)
    return trait if flag else None


# class FemaleTraitBuilder:
#     """Functions common to female trait builders."""
#
#     @staticmethod
#     def should_skip(data, trait):
#         """Check if this record should be skipped because of other fields."""
#         if not data['sex'] or data['sex'][0].value != 'male':
#             return False
#         if data[trait]:
#             data[trait].skipped = "Skipped because sex is 'male'"
#         return True
#
#     @staticmethod
#     def adjust_record(data, trait):
#         """
#         Adjust the trait based on other fields.
#
#         If this is definitely a male then don't flag "gonads" as ambiguous.
#         """
#         if not data['sex'] or data['sex'][0].value != 'female':
#             return
#         for parse in data[trait]:
#             parse.ambiguous_key = False
#
#
# class MaleTraitBuilder:
#     """Functions common to male trait builders."""
#
#     @staticmethod
#     def should_skip(data, trait):
#         """Check if this record should be skipped because of other fields."""
#         if not data['sex'] or data['sex'][0].value != 'female':
#             return False
#         if data[trait]:
#             data[trait].skipped = "Skipped because sex is 'female'"
#         return True
#
#     @staticmethod
#     def adjust_record(data, trait):
#         """
#         Adjust the trait based on other fields.
#
#         If this is definitely a male then don't flag "gonads" as ambiguous.
#         """
#         if not data['sex'] or data['sex'][0].value != 'male':
#             return
#         for parse in data[trait]:
#             parse.ambiguous_key = False
