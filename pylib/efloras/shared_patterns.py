"""Shared plant parser logic."""

import regex
from pylib.shared.patterns import add_frag, add_key, add_rep, add_set, RULE


add_key('sex', 'staminate pistillate'.split())

add_key('plant_part', r"""
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

add_key('leaf', r""" leaf (\s* blades?)? | leaflet | leaves | blades? """)
add_key('petiole', r""" (?<! to \s ) (petioles? | petiolules?)""")
add_key('lobes', r' ( leaf \s* )? (un)?lobe[sd]? ')
add_key('hairs', 'hairs?')
add_key('flower', fr'({RULE["sex"].regexp.pattern} \s+ )? flowers?')
add_key('hypanthium', 'hypan-?thi(um|a)')
add_key('sepal', 'sepals?')
add_key('calyx', 'calyx | calyces')
add_key('stamen', 'stamens?')
add_key('anther', 'anthers?')
add_key('style', 'styles?')
add_key('stigma', 'stigmas?')
add_key('petal', r' petals? ')
add_key('corolla', r' corollas? ')

add_key('shape_starter', """
    broadly
    deeply depressed
    long
    mostly
    narrowly nearly
    partly
    shallowly sometimes
    """.split())

add_frag('location', r""" \b ( terminal | lateral | basal | cauline ) """)
add_key('dim', """ width wide length long radius diameter diam? """.split())

add_frag('punct', r' [,;:/] ', capture=False)

add_key('word', r' [a-z] \w* ', capture=False)


# ############################################################################
# Numeric patterns

add_key('units', ' cm mm '.split())

add_frag('number', r' \d+ ( \. \d* )? ')


# Numeric ranges like: (10–)15–20(–25)
add_rep('range', r"""
    (?<! slash | dash | number )
    (?: open (?P<min> number ) dash close )?
    (?P<low> number )
    (?: dash (?P<high> number ) )?
    (?: open dash (?P<max> number ) close )?
    (?! dash | slash )
    """, capture=False)

add_set('range_set', [
    RULE['units'],
    RULE['number'],
    RULE['dash'],
    RULE['slash'],
    RULE['open'],
    RULE['close'],
    RULE['range']])

# Cross measurements like: 3–5(–8) × 4–11(–13)
# Rename the groups so we can easily extract them in the parsers
RANGE_GROUPS = regex.compile(
    r""" ( min | low | high | max ) """,
    regex.IGNORECASE | regex.VERBOSE)
LENGTH_RANGE = RANGE_GROUPS.sub(r'\1_length', RULE['range'].pattern)
WIDTH_RANGE = RANGE_GROUPS.sub(r'\1_width', RULE['range'].pattern)

add_rep('cross', f"""
    {LENGTH_RANGE} (?P<units_length> units )?
    ( x {WIDTH_RANGE} (?P<units_width> units )? )?
    """, capture=False)
add_set('cross_set', [
    RULE['units'],
    RULE['number'],
    RULE['dash'],
    RULE['slash'],
    RULE['open'],
    RULE['close'],
    RULE['x'],
    RULE['cross']])

CROSS_GROUPS = regex.compile(
    r""" (length | width) """, regex.IGNORECASE | regex.VERBOSE)
CROSS_1 = CROSS_GROUPS.sub(r'\1_1', RULE['cross'].pattern)
CROSS_2 = CROSS_GROUPS.sub(r'\1_2', RULE['cross'].pattern)
add_rep('sex_cross', f"""
    {CROSS_1} (open)? (?P<sex_1> sex )? (close)?
    ( conj | prep )?
    {CROSS_2} (open)? (?P<sex_2> sex )? (close)?
    """, capture=False)
add_set('sex_cross_set', [
    RULE['units'],
    RULE['number'],
    RULE['dash'],
    RULE['slash'],
    RULE['open'],
    RULE['close'],
    RULE['conj'],
    RULE['prep'],
    RULE['x'],
    RULE['sex'],
    RULE['sex_cross']])

# Like "to 10 cm"
add_rep(
    'cross_upper',
    fr""" up_to (?P<high_length> number )
        (?P<units_length> units ) """, capture=False)
add_set('cross_upper_set', [
    RULE['up_to'],
    RULE['units'],
    RULE['number'],
    RULE['cross_upper']])

# Like "to 10"
add_rep('count_upper', fr""" up_to (?P<high> number ) """, capture=False)
add_set('count_upper_set', [
    RULE['up_to'],
    RULE['number'],
    RULE['count_upper']])

# CROSS_DIM = fr"""
#     ( {CROSS_UPPER} | {CROSS} ) ( \s+ (?P<dimension> {DIM}) \b )? """
# add_frag('cross_dim', CROSS_DIM)
