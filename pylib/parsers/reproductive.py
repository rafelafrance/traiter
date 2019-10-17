"""Functions common to most male & female reproductive traits."""

from stacked_regex.token import Token
from stacked_regex.rule import fragment
from pylib.shared_patterns import SHARED
from pylib.numeric_trait import NumericTrait


# Used to get compounds traits from a single parse
TWO_SIDES = fragment(name='two_sides', regexp=f' {SHARED["side"].pattern} ')

# Used to get compounds traits from a single parse
DOUBLE_CROSS = fragment(
    name='double_cross', regexp=f' {SHARED["cross"].pattern} ')


def double(token):
    """Convert a single token into multiple (two) parsers."""
    if not token.groups.get('second'):
        return convert(token)

    # Regex second match groups will overwrite the first match groups
    trait2 = NumericTrait(start=token.start, end=token.end)
    trait2.cross_value(token)
    get_side(trait2, token)

    # We need to re-extract the first match groups
    trait1 = NumericTrait(start=token.start, end=token.end)

    groups = DOUBLE_CROSS.simple_search(token.groups['first'])
    token1 = Token(DOUBLE_CROSS, groups=groups)
    trait1.cross_value(token1)

    groups = TWO_SIDES.simple_search(token.groups['first'])
    token1 = Token(TWO_SIDES, groups=groups)
    get_side(trait1, token1)

    return [trait1, trait2]


def convert(token):
    """Convert parsed token into a trait product."""
    key = [k for k in token.groups.keys() if k.startswith('value2')]
    value2 = token.groups[key[0]] if key else None
    if token.groups.get('ambiguous_char') and not value2:
        return None
    trait = NumericTrait(start=token.start, end=token.end)
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
