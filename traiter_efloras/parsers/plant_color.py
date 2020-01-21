"""Common color snippets."""

import string
from typing import Any
import regex
from traiter_shared.util import FLAGS
from traiter.token import Token
from traiter.vocabulary import Vocabulary
from traiter_shared.trait import Trait
import traiter_efloras.util as util
from traiter_efloras.parsers.base import Base
import traiter_efloras.shared_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)

VOCAB.term('color', r"""
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

VOCAB.term('color_prefix', r"""
    bright(er)? | dark(er)? | deep(er)? | slightly | light(er)? | pale(r)?
    | usually (\s+ not)? | rarely | pale | sometimes | often
    """)

VOCAB.term('color_suffix', r"""
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
        raw_value=token.group['value'])

    for capture in ['location', 'part', 'sex']:
        if capture in token.group:
            setattr(trait, capture, token.group[capture].lower())

    values = util.split_keywords(trait.raw_value)
    values = dict.fromkeys(normalize(v) for v in values)
    trait.value = [v for v in values if v]

    return trait if trait.value else None


def normalize(value: str) -> str:
    """Normalize the shape value."""
    value = VOCAB['shape_starter'].regexp.sub('', value)
    value = value.strip(string.punctuation).lower()

    parts = []
    has_color = False
    for part in regex.split(
            rf'\s+ | {VOCAB["dash"].pattern}', value, flags=FLAGS):
        if VOCAB['color'].regexp.search(part):
            parts.append(RENAME.get(part, part))
            has_color = True
        elif VOCAB['color_suffix'].regexp.search(part):
            parts.append(RENAME.get(part, part))
    if not has_color:
        parts = []

    value = '-'.join(parts)
    value = RENAME.get(value, value)
    return value.strip()


def parser(plant_part):
    """Build a parser for the flower part."""
    catalog = Vocabulary(VOCAB)
    return Base(
        name=f'{plant_part}_color',
        rules=[
            catalog[plant_part],
            catalog['plant_part'],

            catalog.grouper('color_phrase', """
                color_prefix* color color_suffix* """),

            catalog.producer(convert, f"""
                (?P<part> {plant_part} ) (?P<value> color_phrase+ ) """),
        ],
    )


FLOWER_COLOR = parser('flower')
HYPANTHIUM_COLOR = parser('hypanthium')
SEPAL_COLOR = parser('sepal')
PETAL_COLOR = parser('petal')
CAYLX_COLOR = parser('calyx')
COROLLA_COLOR = parser('corolla')
