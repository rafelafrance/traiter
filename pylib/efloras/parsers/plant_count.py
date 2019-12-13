"""Parse the trait."""

from typing import Any
from pylib.stacked_regex.rule import producer, vocab
from pylib.stacked_regex.token import Token
from pylib.efloras.parsers.base import Base
from pylib.shared.trait import Trait
from pylib.efloras.shared_patterns import RULE


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
            RULE[plant_part],
            RULE['plant_part'],
            RULE['count_upper_set'],
            RULE['range_set'],
            vocab('skip', r""" locular [/] """.split()),
            RULE['word'],

            producer(convert, f"""
                (?P<part> {plant_part} ) (word | skip)*
                ( count_upper | range )
                (?! units | cross_joiner | skip )
                """),
            ],
        )


SEPAL_COUNT = parser('sepal')
