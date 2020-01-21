"""Shared plant parser logic."""

import regex
import traiter_shared.patterns as patterns
from traiter.vocabulary import Vocabulary, LOWEST

VOCAB = Vocabulary(patterns.VOCAB)

SEX = r'staminate | pistillate'
VOCAB.term('sex', SEX)

VOCAB.term('plant_part', r"""
    (?<! to \s )
    ( androeci(a|um) | anthers?
    | blades?
    | caly(ces|x) | carpels? | corollas?
    | flowers?
    | gynoeci(a|um)
    | hairs? | hypan-?thi(a|um)
    | leaf | leaflet | leaves | lobes?
    | petals? | petioles? | petiolules? | pistils? | peduncles?
    | ovar(y|ies) | ovules?
    | racemes?
    | sepals? | stamens? | stigmas? | stipules? | styles?
    )""")

VOCAB.term('leaf', r""" leaf (\s* blades?)? | leaflet | leaves | blades? """)
VOCAB.term('petiole', r""" (?<! to \s ) (petioles? | petiolules?)""")
VOCAB.term('lobes', r' ( leaf \s* )? (un)?lobe[sd]? ')
VOCAB.term('hairs', 'hairs?')
VOCAB.term('flower', fr'({SEX} \s+ )? flowers?')
VOCAB.term('hypanthium', 'hypan-?thi(um|a)')
VOCAB.term('sepal', 'sepals?')
VOCAB.term('calyx', 'calyx | calyces')
VOCAB.term('stamen', 'stamens?')
VOCAB.term('anther', 'anthers?')
VOCAB.term('style', 'styles?')
VOCAB.term('stigma', 'stigmas?')
VOCAB.term('petal', r' petals? ')
VOCAB.term('corolla', r' corollas? ')

VOCAB.term('shape_starter', r"""
    broadly
    | deeply | depressed
    | long
    | mostly
    | narrowly | nearly
    | partly
    | shallowly | sometimes
    """)

VOCAB.part('location', r""" \b ( terminal | lateral | basal | cauline ) """)
VOCAB.term('dim', """
    width wide length long radius diameter diam? """.split())

VOCAB.part('punct', r' [,;:/] ', capture=False, priority=LOWEST)

VOCAB.term('word', r' [a-z] \w* ', capture=False, priority=LOWEST)

# ############################################################################
# Numeric patterns

VOCAB.term('units', ' cm mm '.split())

VOCAB.part('number', r' \d+ ( \. \d* )? ')

# Numeric ranges like: (10–)15–20(–25)
RANGE = r"""
    (?<! slash | dash | number )
    (?: open (?P<min> number ) dash close )?
    (?P<low> number )
    (?: dash (?P<high> number ) )?
    (?: open dash (?P<max> number ) close )?
    (?! dash | slash )
    """
VOCAB.grouper('range', RANGE, capture=False)

# Cross measurements like: 3–5(–8) × 4–11(–13)
# Rename the groups so we can easily extract them in the parsers
RANGE_GROUPS = regex.compile(
    r""" ( min | low | high | max ) """,
    regex.IGNORECASE | regex.VERBOSE)
LENGTH_RANGE = RANGE_GROUPS.sub(r'\1_length', RANGE)
WIDTH_RANGE = RANGE_GROUPS.sub(r'\1_width', RANGE)

CROSS = f"""
    {LENGTH_RANGE} (?P<units_length> units )?
    ( x {WIDTH_RANGE} (?P<units_width> units )? )?
    """
VOCAB.grouper('cross', CROSS, capture=False)

CROSS_GROUPS = regex.compile(
    r""" (length | width) """, regex.IGNORECASE | regex.VERBOSE)
CROSS_1 = CROSS_GROUPS.sub(r'\1_1', CROSS)
CROSS_2 = CROSS_GROUPS.sub(r'\1_2', CROSS)
VOCAB.grouper('sex_cross', f"""
    {CROSS_1} (open)? (?P<sex_1> sex )? (close)?
    ( conj | prep )?
    {CROSS_2} (open)? (?P<sex_2> sex )? (close)?
    """, capture=False)

# Like: "to 10 cm"
VOCAB.grouper(
    'cross_upper',
    fr""" up_to (?P<high_length> number )
        (?P<units_length> units ) """, capture=False)

# Like: "to 10"
VOCAB.grouper(
    'count_upper', fr""" up_to (?P<high> number ) """, capture=False)
