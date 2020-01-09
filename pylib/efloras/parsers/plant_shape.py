"""Parse the trait."""

import string
from typing import Any
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.vocabulary import Vocabulary
from pylib.stacked_regex.parser import Parser
import pylib.efloras.util as util
from pylib.efloras.parsers.base import Base
from pylib.shared.trait import Trait
import pylib.efloras.shared_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)

VOCAB.term('plant_shape', r"""
    (\d-)?angular (\d-)?angulate acicular actinomorphic acuminate acute
    apiculate aristate attenuate auriculate
    bilabiate bilateral bilaterally bowl-?shaped
    calceolate campanulate caudate circular convex cordate coronate
    crateriform cruciform cuneate cup-?shaped cupulate cyanthiform
    cylindric(al)? cymbiform
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
    rosettes? rotate rotund round(ed|ish)
    saccate sagittate salverform saucer-?like saucer-?shaped semiterete
    septagonal sinuate spatulate spear-?shaped spheric stellate
    subcylindric(al)? subobtuse suborbicula(r|te) subpeltate subreniform
    subterete subulate symmetric
    terete triangular trullate truncate tubular turbinate
    undulate unifoliate urceolate
    zygomorphic zygomorphous
    """.split())

VOCAB.part('shape_prefix', ' semi | sub | elongate ')

VOCAB.term('leaf_orbicular', r"""
    circular | orbic-?ulate | rotund | round(ed|ish)? | suborbicular
    | suborbiculate
    """)

VOCAB.part('leaf_polygonal', fr"""
    ( ( orbicular | angulate ) -? )?
    ( \b (\d-)? angular | \b (\d-)? angulate
        | pen-?tagonal | pentangular | septagonal )
    ( -? ( orbicular | (\d-)? angulate ) )?
    """)

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


def convert(token: Token) -> Any:
    """Convert parsed token into a trait."""
    trait = Trait(
        start=token.start, end=token.end,
        raw_value=token.groups['value'])

    trait.transfer(token, ['location', 'part', 'sex'])

    values = util.split_keywords(trait.raw_value)

    values = [normalize(v) for v in values]
    values = list(dict.fromkeys(values))  # set() does not preserve order
    trait.value = [v for v in values if v]

    return trait if trait.value else None


def normalize(value: str) -> str:
    """Normalize the shape value."""
    value = VOCAB['shape_starter'].regexp.sub('', value)
    value = VOCAB['location'].regexp.sub('', value)
    value = value.strip(string.punctuation).lower()
    value = VOCAB['leaf_orbicular'].regexp.sub('orbicular', value)
    value = VOCAB['leaf_polygonal'].regexp.sub('polygonal', value)
    value = value.strip()
    value = RENAME.get(value, value)
    value = value if VOCAB['plant_shape'].regexp.search(value) else ''
    return value


def parser(plant_part: str) -> Parser:
    """Build a parser for the flower part."""
    catalog = Vocabulary(VOCAB)
    return Base(
        name=f'{plant_part}_shape',
        rules=[
            catalog[plant_part],
            catalog['plant_part'],

            util.part_phrase(catalog, plant_part),

            catalog.grouper('shape_phrase', """
                ( ( plant_shape | shape_starter | shape_prefix | location )
                  ( punct | conj | prep ){0,2}
                )*
                ( plant_shape | location )
                """),

            catalog.producer(convert, f"""
                    {plant_part}_phrase
                    ( shape_starter? ( word | conj | punct ))*
                    ( word | conj | prep | punct )*
                    (?P<value> shape_phrase )
                    """),
        ])


LEAF_SHAPE = parser('leaf')
PETIOLE_SHAPE = parser('petiole')
FLOWER_SHAPE = parser('flower')
HYPANTHIUM_SHAPE = parser('hypanthium')
SEPAL_SHAPE = parser('sepal')
PETAL_SHAPE = parser('petal')
CAYLX_SHAPE = parser('calyx')
COROLLA_SHAPE = parser('corolla')
