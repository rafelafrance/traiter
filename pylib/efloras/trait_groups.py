"""The trait groups and what is being parsed for each."""

import regex
from pylib.shared.util import FLAGS
from pylib.efloras.parsers.plant_size import LEAF_SIZE, PETIOLE_SIZE
from pylib.efloras.parsers.plant_size import PETAL_SIZE, CALYX_SIZE
from pylib.efloras.parsers.plant_size import SEPAL_SIZE, FLOWER_SIZE
from pylib.efloras.parsers.plant_size import HYPANTHIUM_SIZE, COROLLA_SIZE
from pylib.efloras.parsers.plant_shape import LEAF_SHAPE, PETIOLE_SHAPE
from pylib.efloras.parsers.plant_shape import PETAL_SHAPE, CAYLX_SHAPE
from pylib.efloras.parsers.plant_shape import FLOWER_SHAPE, HYPANTHIUM_SHAPE
from pylib.efloras.parsers.plant_shape import COROLLA_SHAPE, SEPAL_SHAPE
from pylib.efloras.parsers.plant_color import FLOWER_COLOR, HYPANTHIUM_COLOR
from pylib.efloras.parsers.plant_color import SEPAL_COLOR, PETAL_COLOR
from pylib.efloras.parsers.plant_color import CAYLX_COLOR, COROLLA_COLOR
# from pylib.efloras.parsers.plant_count import SEPAL_COUNT

TRAIT_GROUPS = {
    '2n': [],
    'anther heads': [],
    'basal leaves': [
        LEAF_SIZE, LEAF_SHAPE,
        PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'basal rosettes': [],
    'capsules': [],
    'cauline leaves': [
        LEAF_SIZE, LEAF_SHAPE,
        PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'caudices': [],
    'corollas': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'flowering stems': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'flowers': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'fruiting peduncles': [],
    'fruits': [],
    'herbs': [],
    'hypanthia': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'inflorescences': [
        ],
    'inflorescenses': [
        ],
    'leaf blades': [
        LEAF_SIZE, LEAF_SHAPE,
        PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'leaflets': [
        LEAF_SIZE, LEAF_SHAPE,
        PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'leaves': [
        LEAF_SIZE, LEAF_SHAPE,
        PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'pedicels': [],
    'petioles': [
        LEAF_SIZE, LEAF_SHAPE,
        PETIOLE_SIZE, PETIOLE_SHAPE,
        ],
    'peduncles': [],
    'pepos': [],
    'petals': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'pistillate': [],
    'pistillate flowers': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'plants': [],
    'pollen': [],
    'racemes': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'seeds': [],
    'staminate corollas': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'staminate flowers': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'staminate inflorescences': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'staminate racemes': [
        FLOWER_SHAPE, FLOWER_SIZE, FLOWER_COLOR,
        HYPANTHIUM_SHAPE, HYPANTHIUM_SIZE, HYPANTHIUM_COLOR,
        SEPAL_SIZE, SEPAL_SHAPE, SEPAL_COLOR,
        PETAL_SIZE, PETAL_SHAPE, PETAL_COLOR,
        CALYX_SIZE, CAYLX_SHAPE, CAYLX_COLOR,
        COROLLA_SIZE, COROLLA_SHAPE, COROLLA_COLOR,
        ],
    'stolon leaves': [],
    'stolons': [],
    'stems': [],
    'tendrils': [],
    'vines': [],
    'x': [],
    }

TRAIT_GROUP_NAMES = sorted(
    TRAIT_GROUPS.keys(), key=lambda t: (len(t), t), reverse=True)

TRAIT_GROUPS_RE = ' | '.join(
    r' \s+ '.join(x.split()) for x in TRAIT_GROUP_NAMES)
TRAIT_GROUPS_RE = regex.compile(
    rf"""
        (?<! [\w:;,<>()] \s ) (?<! [\w:;,<>()] )
        \b ( {TRAIT_GROUPS_RE} ) \b
        """,
    flags=FLAGS)

TRAIT_NAMES = sorted({t.name for g in TRAIT_GROUPS.values() for t in g})
