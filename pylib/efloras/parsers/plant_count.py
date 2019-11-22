"""Parse the trait."""

from typing import Any
from pylib.stacked_regex.rule import producer, keyword
from pylib.stacked_regex.token import Token
from pylib.efloras.parsers.base import Base
from pylib.efloras.trait import Trait
import pylib.efloras.shared_plant as plant


def convert(token: Token) -> Any:
    """Convert parsed token into a trait."""
    trait = Trait(start=token.start, end=token.end)

    if 'location' in token.groups:
        trait.location = token.groups['location'].lower()

    if 'part' in token.groups:
        trait.part = token.groups['part'].lower()

    for key in ['min', 'low', 'high', 'max']:
        if key in token.groups:
            setattr(trait, key, float(token.groups[key]))

    return trait


def parser(plant_part):
    """Build a parser for the flower part."""
    return Base(
        name=f'{plant_part}_count',
        rules=[
            plant.RULE[plant_part],
            plant.RULE['plant_part'],
            plant.RULE['count_upper'],
            plant.RULE['range'],
            plant.RULE['units'],
            plant.RULE['cross_joiner'],
            keyword('skip', r""" locular [/] """.split()),
            plant.RULE['word'],

            producer(convert, f"""
                (?P<part> {plant_part} ) (word | skip)*
                ( count_upper | range )
                (?! units | cross_joiner | skip )
                """),
            ],
        )


SEPAL_COUNT = parser('sepal')
