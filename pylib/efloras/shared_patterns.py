"""Shared plant parser logic."""

import regex
import pylib.shared.patterns as patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog


CAT = RuleCatalog(patterns.CAT)
RULE = CAT.rules


SEX = 'staminate pistillate'.split()
CAT.term('sex', SEX)

CAT.term('plant_part', r"""
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

CAT.term('leaf', r""" leaf (\s* blades?)? | leaflet | leaves | blades? """)
CAT.term('petiole', r""" (?<! to \s ) (petioles? | petiolules?)""")
CAT.term('lobes', r' ( leaf \s* )? (un)?lobe[sd]? ')
CAT.term('hairs', 'hairs?')
CAT.term('flower', fr'({SEX} \s+ )? flowers?')
CAT.term('hypanthium', 'hypan-?thi(um|a)')
CAT.term('sepal', 'sepals?')
CAT.term('calyx', 'calyx | calyces')
CAT.term('stamen', 'stamens?')
CAT.term('anther', 'anthers?')
CAT.term('style', 'styles?')
CAT.term('stigma', 'stigmas?')
CAT.term('petal', r' petals? ')
CAT.term('corolla', r' corollas? ')

CAT.term('shape_starter', """
    broadly
    deeply depressed
    long
    mostly
    narrowly nearly
    partly
    shallowly sometimes
    """.split())

CAT.part('location', r""" \b ( terminal | lateral | basal | cauline ) """)
CAT.term('dim', """
    width wide length long radius diameter diam? """.split())

CAT.part('punct', r' [,;:/] ', capture=False)

CAT.term('word', r' [a-z] \w* ', capture=False)


# ############################################################################
# Numeric patterns

CAT.term('units', ' cm mm '.split())

CAT.part('number', r' \d+ ( \. \d* )? ')


# Numeric ranges like: (10–)15–20(–25)
RANGE = r"""
    (?<! slash | dash | number )
    (?: open (?P<min> number ) dash close )?
    (?P<low> number )
    (?: dash (?P<high> number ) )?
    (?: open dash (?P<max> number ) close )?
    (?! dash | slash )
    """
CAT.grouper('range', RANGE, capture=False)


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
CAT.grouper('cross', CROSS, capture=False)


CROSS_GROUPS = regex.compile(
    r""" (length | width) """, regex.IGNORECASE | regex.VERBOSE)
CROSS_1 = CROSS_GROUPS.sub(r'\1_1', CROSS)
CROSS_2 = CROSS_GROUPS.sub(r'\1_2', CROSS)
CAT.grouper('sex_cross', f"""
    {CROSS_1} (open)? (?P<sex_1> sex )? (close)?
    ( conj | prep )?
    {CROSS_2} (open)? (?P<sex_2> sex )? (close)?
    """, capture=False)

# Like "to 10 cm"
CAT.grouper(
    'cross_upper',
    fr""" up_to (?P<high_length> number )
        (?P<units_length> units ) """, capture=False)


# Like "to 10"
CAT.grouper('count_upper', fr""" up_to (?P<high> number ) """, capture=False)
