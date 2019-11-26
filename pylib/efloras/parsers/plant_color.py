"""Common color snippets."""

import string
from typing import Any
import regex
from pylib.shared.util import FLAGS
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import keyword, grouper, producer
from pylib.efloras.trait import Trait
import pylib.efloras.util as util
from pylib.efloras.parsers.base import Base
from pylib.efloras.shared_patterns import RULE


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

    values = util.split_keywords(trait.raw_value)

    values = [normalize(v) for v in values]
    values = list(dict.fromkeys(values))
    trait.value = [v for v in values if v]

    return trait if trait.value else None


def normalize(value: str) -> str:
    """Normalize the shape value."""
    value = RULE['shape_starter'].regexp.sub('', value)
    value = value.strip(string.punctuation).lower()

    parts = []
    has_color = False
    for part in regex.split(
            rf'\s+ | {RULE["dash"].pattern}', value, flags=FLAGS):
        if COLORS.regexp.search(part):
            parts.append(RENAME.get(part, part))
            has_color = True
        elif COLOR_SUFFIX.regexp.search(part):
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
        rules=[
            RULE[plant_part],
            RULE['plant_part'],
            COLORS,
            COLOR_PREFIX,
            COLOR_SUFFIX,

            grouper('color_phrase', """
                color_prefix*
                flower_color
                color_suffix*
                """),

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
