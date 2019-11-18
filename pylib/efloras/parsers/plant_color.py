"""Common color snippets."""

import re
import string
from typing import Any
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import keyword, replacer, producer
from pylib.efloras.trait import Trait
import pylib.efloras.util as util
from pylib.efloras.parsers.base import Base
import pylib.efloras.shared_plant as plant


COLORS = keyword('flower_color', r"""
    black(ish)? blue(ish)? brown brownish
    cream cream-yellow creamy
    crimson
    glaucous-pink gold golden golden-yellow gray gray-green green greenish 
    grey grey-green
    ivory ivory-white
    lavendar lavender lemon lilac
    maroon
    olive olive-green orange orange-pink
    pink pink-purple pink-violet pinkish purple purpleish purplish
    red red-brown reddish rose rose-coloured
    salmon salmon-pink scarlet silvery? stramineous straw-colored 
    sulphur-yellow
    tan
    violet violetish
    white whitish
    yellow yellowish
    """.split())

COLOR_PREFIX = keyword('color_prefix', r"""
    bright(er)? | dark(er)? | deep(er)? | slightly | light(er)? | pale(r)?
    | usually (\s+ not)? | rarely | pale | sometimes | often
    """)

COLOR_SUFFIX = keyword('color_suffix', r"""
    spotted spots? stripe(s|d)? vein(s|ed)? tip(s|ped)? mottled
    tinge(s|d)? longitudinal throated lined """.split())

RENAME = {
    'blackish': 'black',
    'blueish': 'blue',
    'brownish': 'brown',
    'cream': 'white',
    'cream-yellow': 'yellow',
    'creamy': 'cream',
    'crimson': 'red',
    'glaucous-pink': 'pink',
    'golden-yellow': 'yellow',
    'greyish': 'gray',
    'greenish': 'green',
    'ivory': 'white',
    'lavendar': 'purple',
    'lavender': 'purple',
    'lemon': 'yellow',
    'lilac': 'purple',
    'maroon': 'red-brown',
    'olive-green': 'green',
    'pink-violet': 'pink-purple',
    'pinkish': 'pink',
    'purpleish': 'purple',
    'purplish': 'purple',
    'reddish': 'red',
    'rose': 'pink',
    'rose-coloured': 'pink',
    'salmon-pink': 'orange-pink',
    'scarlet': 'red',
    'silvery': 'silver',
    'stramineous': 'yellow',
    'straw-colored': 'yellow',
    'sulphur-yellow': 'yellow',
    'violet': 'purple',
    'violetish': 'purple',
    'whitish': 'white',
    'yellowish': 'yellow',
    }


def convert(token: Token) -> Any:
    """Convert parsed token into a trait."""
    trait = Trait(
        start=token.start, end=token.end,
        raw_value=token.groups['value'])

    if 'location' in token.groups:
        trait.location = token.groups['location'].lower()

    if 'part' in token.groups:
        trait.part = token.groups['part'].lower()

    if 'sex' in token.groups:
        trait.sex = token.groups['sex'].lower()

    values = plant.split_keywords(trait.raw_value)

    values = [normalize(v) for v in values]
    values = list(dict.fromkeys(values))
    trait.value = [v for v in values if v]

    return trait if trait.value else None


def normalize(value: str) -> str:
    """Normalize the shape value."""
    value = plant.SCANNER['shape_starter'].regex.sub('', value)
    value = value.strip(string.punctuation).lower()

    parts = []
    has_color = False
    for part in re.split(rf'\s+ | {plant.DASH}', value, flags=util.FLAGS):
        if COLORS.regex.search(part):
            parts.append(RENAME.get(part, part))
            has_color = True
        elif COLOR_SUFFIX.regex.search(part):
            parts.append(RENAME.get(part, part))
    if not has_color:
        parts = []

    value = '-'.join(parts)
    value = RENAME.get(value, value)
    return value.strip()


def parser(plant_part):
    """Build a parser for the flower part."""
    return Base(
        name=f'{plant_part}_color',
        scanners=[
            plant.SCANNER[plant_part],
            plant.SCANNER['plant_part'],
            COLORS,
            COLOR_PREFIX,
            COLOR_SUFFIX,
            ],
        replacers=[
            replacer('color_phrase', """
                color_prefix*
                flower_color
                color_suffix*
                """),
            ],
        producers=[
            producer(convert, f"""
                (?P<part> {plant_part} ) (?P<value> color_phrase+ ) """),
            ],
        )


FLOWER_COLOR = parser('flower')
HYPANTHIUM_COLOR = parser('hypanthium')
SEPAL_COLOR = parser('sepal')
PETAL_COLOR = parser('petal')
CAYLX_COLOR = parser('calyx')
COROLLA_COLOR = parser('corolla')
