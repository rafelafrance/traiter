"""Functions common to most male & female reproductive traits."""

from string import punctuation
from copy import copy
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

    trait2 = Trait(start=token.start, end=token.end)
    token2 = Token(DOUBLE_CROSS, groups=copy(token.groups))

    values1 = trait1.all_values(
        token1, ['value1_1', 'value2a_1', 'value2b_1', 'value2c_1'])
    values2 = trait2.all_values(
        token2, ['value1_2', 'value2a_2', 'value2b_2', 'value2c_2'])

    units1 = trait1.first_value(
        token1, ['units1a_1', 'units1b_1', 'units1c_1', 'units2_1'])
    units2 = trait2.first_value(
        token2, ['units1a_2', 'units1b_2', 'units1c_2', 'units2_2'])

    side1 = trait1.first_value(token1, ['side1_1', 'side2_1'])
    side2 = trait2.first_value(token2, ['side1_2', 'side2_2'])
    side1 = side1.lower().strip(punctuation) if side1 else None
    side2 = side2.lower().strip(punctuation) if side2 else None
    side1 = SIDES.get(side2) if not side1 else side1
    side2 = SIDES.get(side1) if not side2 else side2

    trait1.float_value(*values1)  # pylint: disable=no-value-for-parameter
    trait2.float_value(*values2)  # pylint: disable=no-value-for-parameter

    if units1 and units2:
        trait1.convert_value(units1)
        trait2.convert_value(units2)
    elif units1 and not units2:
        trait1.convert_value(units1)
        trait2.convert_value(units1)
    elif units2 and not units1:
        trait1.convert_value(units2)
        trait2.convert_value(units2)

    if side1:
        setattr(trait1, 'side', side1)
    if side2:
        setattr(trait2, 'side', side2)

    return [trait1, trait2]


def convert(token):
    """Convert parsed token into a trait product."""
    trait = Trait(start=token.start, end=token.end)

    trait.cross_value(token)
    trait.is_flag_in_token('ambiguous_char', token, rename='ambiguous_key')
    trait.is_flag_in_token('ambiguous_key', token)
    trait.is_value_in_token('dimension', token)
    trait.is_value_in_token('dim', token, rename='dimension')
    get_side(trait, token)
    return trait


def get_side(trait, token):
    """Get the side token."""
    trait.is_value_in_token('side', token)
    trait.is_value_in_token('side1', token, 'side')
    trait.is_value_in_token('side2', token, 'side')


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
