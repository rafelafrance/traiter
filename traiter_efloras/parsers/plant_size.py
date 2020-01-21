"""Parse the trait."""

import copy
from typing import Any
from traiter_shared.util import to_float
from traiter_shared.trait import Trait
from traiter_shared.convert_units import convert as convert_units
from traiter.token import Token
from traiter.vocabulary import Vocabulary
import traiter_efloras.util as util
from traiter_efloras.parsers.base import Base
from traiter_efloras.shared_patterns import VOCAB


def convert(token: Token) -> Any:
    """Convert parsed token into a trait."""
    trait = Trait(start=token.start, end=token.end)

    trait.transfer(token, ['location', 'part', 'sex', 'dimension'])

    valid = set_size_values(trait, token)
    return trait if valid else None


def sex_convert(token: Token) -> Any:
    """Convert two crosses assigned to the sexes."""
    token1 = remove_suffix(token, '_1')
    trait1 = convert(token1)

    token2 = remove_suffix(token, '_2')
    trait2 = convert(token2)

    return [trait1, trait2]


def remove_suffix(token, suffix):
    """
    Convert multi-part token to single-part token by stripping group suffixes.

    Some forms capture multiple values at the same time differentiated by
    suffixes like: length_1, units_1, length_2. This "lowers" one of the parts
    by copying the values from length_1 and units_1 to length and units. This
    allows us to reuse conversion code designed for group names w/o suffixes.
    """
    new_token = Token(
        rule=token.rule,
        group=copy.copy(token.group),
        span=(token.start, token.end))
    new = {k[:-2]: v for k, v in token.group.items() if k.endswith(suffix)}
    new_token.group.update(new)
    return new_token


def set_size_values(trait, token):
    """
    Update the size measurements with normalized values.

    There are typically several measurements (minimum, low, high, & maximum)
    for each dimension (length & width). We normalize to millimeters.
    """
    length = token.group.get('units_length', '')
    width = token.group.get('units_width', '')

    # No units means it's not a measurement
    if not (length or width):
        return False

    units = {
        'length': length if length else width,
        'width': width if width else length}

    for dim in ('length', 'width'):
        for value in ('min', 'low', 'high', 'max'):
            key = f'{value}_{dim}'
            if key in token.group:
                norm = convert_units(to_float(token.group[key]), units[dim])
                setattr(trait, key, norm)

    return True


def parser(plant_part):
    """Build a parser for the plant part."""
    catalog = Vocabulary(VOCAB)
    return Base(
        name=f'{plant_part}_size',
        rules=[
            catalog[plant_part],
            catalog['plant_part'],

            catalog.grouper(
                'noise', """
                (?: word | number | dash | punct | up_to | dim | slash
                    | conj )*? """,
                capture=False),

            util.part_phrase(catalog, plant_part),

            catalog.producer(sex_convert, f"""
                {plant_part}_phrase noise sex_cross """),

            catalog.producer(convert, f"""
                {plant_part}_phrase noise (?: open? sex close? )? noise
                    (?: cross_upper | cross ) (?P<dimension> dim )? """),
        ],
    )


LEAF_SIZE = parser('leaf')
PETIOLE_SIZE = parser('petiole')
SEPAL_SIZE = parser('sepal')
PETAL_SIZE = parser('petal')
CALYX_SIZE = parser('calyx')
COROLLA_SIZE = parser('corolla')
FLOWER_SIZE = parser('flower')
HYPANTHIUM_SIZE = parser('hypanthium')
