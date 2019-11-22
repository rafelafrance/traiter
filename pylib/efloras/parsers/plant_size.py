"""Parse the trait."""

import copy
from typing import Any
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import producer
from pylib.efloras.trait import Trait
from pylib.efloras.parsers.base import Base
import pylib.efloras.shared_plant as plant


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

    valid = plant.set_size_values(trait, token)
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


def leaf_parser(plant_part):
    """Build a parser for the plant part."""
    return Base(
        name=f'{plant_part}_size',
        rules=[
            plant.RULE[plant_part],
            plant.RULE['plant_part'],
            plant.RULE['sex_cross'],
            plant.RULE['sex'],
            plant.RULE['cross_dim'],
            plant.RULE['dim'],
            plant.RULE['location'],

            plant.part_phrase(plant_part),

            producer(sex_convert, f"""
                {plant_part}_phrase dim* sex_cross """),
            producer(convert, f"""
                {plant_part}_phrase sex* cross_dim """),
            producer(convert, f"""
                {plant_part}_phrase dim* cross_dim sex? """),
            ],
        )


def flower_parser(plant_part):
    """Build a parser for the plant part."""
    return Base(
        name=f'{plant_part}_size',
        rules=[
            plant.RULE[plant_part],
            plant.RULE['plant_part'],
            plant.RULE['sex_cross'],
            plant.RULE['sex'],
            plant.RULE['cross_dim'],
            plant.RULE['dim'],

            producer(sex_convert, f"""
                (?P<part> {plant_part} ) dim* sex_cross """),
            producer(convert, f"""
                (?P<part> {plant_part} ) dim*
                    cross_dim (?P<dimension> dim )?  sex? """),
            ],
        )


LEAF_SIZE = leaf_parser('leaf')
PETIOLE_SIZE = leaf_parser('petiole')
SEPAL_SIZE = leaf_parser('sepal')
PETAL_SIZE = leaf_parser('petal')
CALYX_SIZE = leaf_parser('calyx')
COROLLA_SIZE = leaf_parser('corolla')

FLOWER_SIZE = flower_parser('flower')
HYPANTHIUM_SIZE = flower_parser('hypanthium')
