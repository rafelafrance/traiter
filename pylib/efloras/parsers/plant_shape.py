"""Parse the trait."""

import string
from typing import Any
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import fragment, keyword, replacer, producer
from pylib.efloras.parsers.base import Base
from pylib.efloras.trait import Trait
import pylib.efloras.shared_plant as plant


SHAPE = fragment('plant_shape', r"""
    (\d-)?angular (\d-)?angulate acicular actinomorphic acuminate acute
    apiculate aristate attenuate auriculate
    bilabiate bilateral bilaterally bowl-?shaped
    calceolate campanulate caudate circular convex cordate coronate
    crateriform cruciform cuneate cup-?shaped cupulate cyanthiform cylindric
    cymbiform
    deltate deltoid dentate depressed digitate
    elliptic elongate emarginate ensate ensiform
    falcate fenestrate filiform flabellate flabelliorm funnelform
    galeate globose
    hastate hemispheric
    incised infundibular irregular(ly)?
    keeled
    labiate laciniate lanceolate ligulate liguliform linear lorate lyrate
    monosymmetric monosymmetrical mucronate multifid
    navicular
    obconic obcordate oblanceolate oblique oblong obovate obtriangular obtuse
    orbic-?ular orbic-?ulate orbicular ovate
    palmatifid palmatipartite palmatisect pandurate
    papilionaceous peltate pen-?tagonal pentangular perfoliate
    perforate petiolate pinnate(?!ly) pinnatifid pinnatipartite pinnatisect
    plicate polygonal
    radially rectangular regular reniform retuse rhombic rhomboid rhomboidal
    rosettes? rotate rotund round rounded roundish
    saccate sagittate salverform saucer-?like saucer-?shaped septagonal sinuate
    spatulate spear-?shaped spheric stellate subobtuse suborbiculate subulate
    symmetric
    terete triangular trullate truncate tubular turbinate
    undulate unifoliate urceolate
    zygomorphic zygomorphous
    """.split())

RENAME = {
    'actinomorphic': 'radially symmetric',
    'angular-orbiculate': 'polygonal',
    'bilateral': 'bilaterally symmetric',
    'bowl-shaped': 'saucerlike',
    'bowlshaped': 'saucerlike',
    'crateriform': 'saucerlike',
    'cupulate': 'cup-shaped',
    'cyanthiform': 'saucerlike',
    'deltate': 'deltoid',
    'ensiform': 'linear',
    'flabelliorm': 'flabellate',
    'globose': 'spheric',
    'irregular': 'bilaterally symmetric',
    'irregularly': 'bilaterally symmetric',
    'keeled': 'cymbiform',
    'labiate': 'bilabiate',
    'liguliform': 'ligulate',
    'lorate': 'linear',
    'monosymmetric': 'bilaterally symmetric',
    'monosymmetrical': 'bilaterally symmetric',
    'navicular': 'cymbiform',
    'oblong-terete': 'oblong',
    'palmately': 'palmate',
    'pedately': 'pedate',
    'rectangular': 'rhomboid',
    'regular': 'radially symmetric',
    'rhombic': 'rhomboic',
    'saucer-shaped': 'saucerlike',
    'saucershaped': 'saucerlike',
    'subcylindric': 'cylindrical',
    'subcylindrical': 'cylindrical',
    'subreniform': 'reniform',
    'zygomorphic': 'bilaterally symmetric',
    'zygomorphous': 'bilaterally symmetric',
    }

ORBICULAR = keyword('leaf_orbicular', r"""
    circular | orbic-?ulate | rotund | round(ed|ish)? | suborbicular
    | suborbiculate
    """)

POLYGONAL = fragment('leaf_polygonal', fr"""
    ( ( orbicular | angulate ) -? )?
    ( \b (\d-)? angular | \b (\d-)? angulate
        | pen-?tagonal | pentangular | septagonal )
    ( -? ( orbicular | (\d-)? angulate ) )?
    """)

SHAPE_PREFIX = fragment('shape_prefix', ' semi | sub | elongate ')


def convert(token: Token) -> Any:
    """Convert parsed token into a trait."""
    trait = Trait(
        start=token.start, end=token.end,
        raw_value=token.groups['value'])

    if 'location' in token.groups:
        trait.location = token.groups['location']

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
    value = plant.SCANNER['location'].regex.sub('', value)
    value = value.strip(string.punctuation).lower()
    value = ORBICULAR.regex.sub('orbicular', value)
    value = POLYGONAL.regex.sub('polygonal', value)
    value = value.strip()
    value = RENAME.get(value, value)
    value = value if SHAPE.regex.search(value) else ''
    return value


def parser(plant_part):
    """Build a parser for the flower part."""
    return Base(
        name=f'{plant_part}_shape',
        scanners=[
            plant.SCANNER[plant_part],
            plant.SCANNER['plant_part'],
            plant.SCANNER['location'],
            SHAPE,
            plant.SCANNER['shape_starter'],
            SHAPE_PREFIX,
            plant.SCANNER['conj'],
            plant.SCANNER['prep'],
            plant.SCANNER['word'],
            ],
        replacers=[
            plant.part_phrase(plant_part),
            replacer('shape_phrase', """
                ( plant_shape | shape_starter | shape_prefix | location )*
                plant_shape
                """),
            replacer('noise', ' word | shape_starter noise '),
            ],
        producers=[
            producer(convert, f"""
                {plant_part}_phrase
                ( noise | conj | prep )*
                (?P<value>
                    ( shape_phrase | shape_starter | shape_prefix
                        | conj | prep | noise
                    )*
                    shape_phrase ((shape_starter | conj | prep)* location)?
                )
                """),
            ],
        )


LEAF_SHAPE = parser('leaf')
PETIOLE_SHAPE = parser('petiole')
FLOWER_SHAPE = parser('flower')
HYPANTHIUM_SHAPE = parser('hypanthium')
SEPAL_SHAPE = parser('sepal')
PETAL_SHAPE = parser('petal')
CAYLX_SHAPE = parser('calyx')
COROLLA_SHAPE = parser('corolla')
