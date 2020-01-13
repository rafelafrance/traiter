"""Parse the trait."""

from typing import Any
from pylib.stacked_regex.vocabulary import Vocabulary
from pylib.stacked_regex.token import Token
from pylib.efloras.parsers.base import Base
from pylib.shared.trait import Trait
import pylib.efloras.shared_patterns as patterns


def convert(token: Token) -> Any:
    """Convert parsed token into a trait."""
    trait = Trait(start=token.start, end=token.end)

    if 'location' in token.group:
        trait.location = token.group['location'].lower()

    if 'part' in token.group:
        trait.part = token.group['part'].lower()

    for key in ['min', 'low', 'high', 'max']:
        if key in token.group:
            setattr(trait, key, float(token.group[key]))

    return trait


def parser(plant_part):
    """Build a parser for the flower part."""
    catalog = Vocabulary(patterns.VOCAB)
    return Base(
        name=f'{plant_part}_count',
        rules=[
            catalog[plant_part],
            catalog['plant_part'],
            catalog.term('skip', r""" locular [/] """.split()),

            catalog.producer(convert, f"""
                (?P<part> {plant_part} ) (word | skip)*
                ( count_upper | range )
                (?! units | cross_joiner | skip )
                """),
        ],
    )


SEPAL_COUNT = parser('sepal')
