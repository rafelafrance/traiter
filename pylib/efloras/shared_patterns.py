"""Shared plant parser logic."""

import regex
import pylib.shared.patterns as patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog, LAST

CATALOG = RuleCatalog(patterns.CATALOG)

SEX = r'staminate | pistillate'
CATALOG.term('sex', SEX)

CATALOG.term('plant_part', r"""
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

CATALOG.term('leaf', r""" leaf (\s* blades?)? | leaflet | leaves | blades? """)
CATALOG.term('petiole', r""" (?<! to \s ) (petioles? | petiolules?)""")
CATALOG.term('lobes', r' ( leaf \s* )? (un)?lobe[sd]? ')
CATALOG.term('hairs', 'hairs?')
CATALOG.term('flower', fr'({SEX} \s+ )? flowers?')
CATALOG.term('hypanthium', 'hypan-?thi(um|a)')
CATALOG.term('sepal', 'sepals?')
CATALOG.term('calyx', 'calyx | calyces')
CATALOG.term('stamen', 'stamens?')
CATALOG.term('anther', 'anthers?')
CATALOG.term('style', 'styles?')
CATALOG.term('stigma', 'stigmas?')
CATALOG.term('petal', r' petals? ')
CATALOG.term('corolla', r' corollas? ')

CATALOG.term('shape_starter', r"""
    broadly
    | deeply | depressed
    | long
    | mostly
    | narrowly | nearly
    | partly
    | shallowly | sometimes
    """)

CATALOG.part('location', r""" \b ( terminal | lateral | basal | cauline ) """)
CATALOG.term('dim', """
    width wide length long radius diameter diam? """.split())

CATALOG.part('punct', r' [,;:/] ', capture=False, when=LAST)

CATALOG.term('word', r' [a-z] \w* ', capture=False, when=LAST)

# ############################################################################
# Numeric patterns

CATALOG.term('units', ' cm mm '.split())

CATALOG.part('number', r' \d+ ( \. \d* )? ')

# Numeric ranges like: (10–)15–20(–25)
RANGE = r"""
    (?<! slash | dash | number )
    (?: open (?P<min> number ) dash close )?
    (?P<low> number )
    (?: dash (?P<high> number ) )?
    (?: open dash (?P<max> number ) close )?
    (?! dash | slash )
    """
CATALOG.grouper('range', RANGE, capture=False)

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
CATALOG.grouper('cross', CROSS, capture=False)

CROSS_GROUPS = regex.compile(
    r""" (length | width) """, regex.IGNORECASE | regex.VERBOSE)
CROSS_1 = CROSS_GROUPS.sub(r'\1_1', CROSS)
CROSS_2 = CROSS_GROUPS.sub(r'\1_2', CROSS)
CATALOG.grouper('sex_cross', f"""
    {CROSS_1} (open)? (?P<sex_1> sex )? (close)?
    ( conj | prep )?
    {CROSS_2} (open)? (?P<sex_2> sex )? (close)?
    """, capture=False)

# Like: "to 10 cm"
CATALOG.grouper(
    'cross_upper',
    fr""" up_to (?P<high_length> number )
        (?P<units_length> units ) """, capture=False)

# Like: "to 10"
CATALOG.grouper(
    'count_upper', fr""" up_to (?P<high> number ) """, capture=False)
