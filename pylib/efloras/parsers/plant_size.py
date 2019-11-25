"""Parse the trait."""

import copy
from typing import Any
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import producer, grouper
import pylib.efloras.util as util
from pylib.efloras.trait import Trait
from pylib.efloras.parsers.base import Base
from pylib.efloras.shared_patterns import RULE


def convert(token: Token) -> Any:
    """Convert parsed token into a trait."""
    trait = Trait(start=token.start, end=token.end)

    if 'location' in token.groups:
        trait.location = token.groups['location'].lower()

    if 'part' in token.groups:
        trait.part = token.groups['part'].lower()

    if 'sex' in token.groups:
        trait.sex = token.groups['sex'].lower()

    if 'dimension' in token.groups:
        trait.dimension = token.groups['dimension']

    valid = set_size_values(trait, token)
    return trait if valid else None


def sex_convert(token: Token) -> Any:
    """Convert two crosses assigned to the sexes."""
    token1 = Token(
        rule=token.rule,
        groups=copy.copy(token.groups),
        span=(token.start, token.end))
    new = {k[:-2]: v for k, v in token.groups.items() if k.endswith('_1')}
    token1.groups.update(new)

    trait1 = convert(token1)

    token2 = Token(
        rule=token.rule,
        groups=copy.copy(token.groups),
        span=(token.start, token.end))
    new = {k[:-2]: v for k, v in token.groups.items() if k.endswith('_2')}
    token2.groups.update(new)
    trait2 = convert(token2)

    return [trait1, trait2]


def set_size_values(trait, token):
    """Update the size measurements with normalized values."""
    units, multiplier = {}, {}

    units['length'] = token.groups.get('units_length', '').lower()
    units['width'] = token.groups.get('units_width', '').lower()

    # No units means it's not a measurement
    if not (units['length'] or units['width']):
        return False

    if not units['length']:
        multiplier['width'] = 10.0 if units['width'] == 'cm' else 1.0
        multiplier['length'] = multiplier['width']
    elif not units['width']:
        multiplier['length'] = 10.0 if units['length'] == 'cm' else 1.0
        multiplier['width'] = multiplier['length']
    else:
        multiplier['length'] = 10.0 if units['length'] == 'cm' else 1.0
        multiplier['width'] = 10.0 if units['width'] == 'cm' else 1.0

    for dimension in ['length', 'width']:
        for value in ['min', 'low', 'high', 'max']:
            key = f'{value}_{dimension}'
            if key in token.groups:
                setattr(trait, key,
                        float(token.groups[key]) * multiplier[dimension])
    return True


def parser(plant_part):
    """Build a parser for the plant part."""
    return Base(
        name=f'{plant_part}_size',
        rules=[
            RULE[plant_part],
            RULE['plant_part'],
            RULE['cross_set'],
            RULE['cross_upper_set'],
            RULE['sex_cross_set'],
            RULE['dim'],
            RULE['location'],

            grouper(
                'noise', """
                (?: word | number | dash | punct | up_to | dim | slash
                    | conj )*? """,
                capture=False),

            util.part_phrase(plant_part),

            producer(sex_convert, f"""
                {plant_part}_phrase noise sex_cross """),

            producer(convert, f"""
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
