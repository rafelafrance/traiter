"""Shared plant parser logic."""

import re
from pylib.stacked_regex.rule import fragment, keyword, replacer
import pylib.efloras.util as util


SCANNER = {}


def add_frag(name: str, regexp: str) -> None:
    """Add a rule to SCANNER."""
    SCANNER[name] = fragment(name, regexp)


def add_key(name: str, regexp: str) -> None:
    """Add a rule to SCANNER."""
    SCANNER[name] = keyword(name, regexp)


SEX = 'staminate | pistillate'
add_key('sex', SEX)

CONJ = ' or | and '
add_key('conj', CONJ)
PREP = ' to | with '
add_key('prep', PREP)

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
    )
    """)

add_key('leaf', r""" leaf (\s* blades?)? | leaflet | leaves | blades? """)
add_key(
    'petiole', r""" (?<! to \s ) (petioles? | petiolules?)""")
add_key('lobes', r' ( leaf \s* )? (un)?lobe[sd]? ')
add_key('hairs', 'hairs?')
add_key('flower', fr'({SCANNER["sex"].regex.pattern} \s+ )? flowers?')
add_key('hypanthium', 'hypan-?thi(um|a)')
add_key('sepal', 'sepals?')
add_key('calyx', 'calyx | calyces')
add_key('stamen', 'stamens?')
add_key('anther', 'anthers?')
add_key('style', 'styles?')
add_key('stigma', 'stigmas?')
add_key('petal', r' petals? ')
add_key('corolla', r' corollas? ')

add_key('shape_starter', r"""
    broadly
    deeply depressed 
    long
    mostly
    narrowly nearly
    partly
    shallowly sometimes
    """.split())

add_frag('location', r""" \b ( terminal | lateral | basal | cauline ) """)

add_frag('punct', r' [,;:/] ')

DIM = """ width | wide | length | long | radius | diameter | diam? """
add_key('dim', DIM)
add_key('word', r' [a-z] \w* ')


# ############################################################################
# Numeric patterns

UNITS = r' cm | mm '
add_key('units', UNITS)

NUMBER = r' \d+ ( \. \d* )? '
add_frag('number', NUMBER)

DASH = r' (?: – | - ) '
add_frag('dash', DASH)

OPEN = r' [(\[] '
CLOSE = r' [)\]] '
add_frag('open', OPEN)
add_frag('close', CLOSE)

# Numeric ranges like: (10–)15–20(–25)
RANGE = fr"""
    (?<! [/\d\-] )
    (?: {OPEN} \s* (?P<min> {NUMBER} ) \s* {DASH} \s* {CLOSE} \s* )?
    (?P<low> {NUMBER} )
    (?: \s* {DASH} \s* (?P<high> {NUMBER} ) )?
    (?: \s* {OPEN} \s* {DASH} \s* (?P<max> {NUMBER} ) \s* {CLOSE} )?
    """
add_frag('range', RANGE)

# Cross measurements like: 3–5(–8) × 4–11(–13)
CROSS_JOINER = r' x | × '
add_frag('cross_joiner', CROSS_JOINER)

# Rename the groups so we can easily extract them in the parsers
RANGE_GROUPS = re.compile(
    r""" ( min | low | high | max ) """,
    re.IGNORECASE | re.VERBOSE)
LENGTH_RANGE = RANGE_GROUPS.sub(r'\1_length', RANGE)
WIDTH_RANGE = RANGE_GROUPS.sub(r'\1_width', RANGE)

CROSS = fr"""
    (?P<length> {LENGTH_RANGE} (?! \S) 
        ( \s* (?P<units_length> {UNITS} ) )? )
    (?: \s* (?: {CROSS_JOINER} ) \s*
    (?P<width> {WIDTH_RANGE} (?! \S) 
        ( \s* (?P<units_width> {UNITS} ) )? )
        )?
    """
add_frag('cross', CROSS)

CROSS_GROUPS = re.compile(
    r""" (length | width) """, re.IGNORECASE | re.VERBOSE)
CROSS_1 = CROSS_GROUPS.sub(r'\1_1', CROSS)
CROSS_2 = CROSS_GROUPS.sub(r'\1_2', CROSS)
SEX_CROSS = fr"""
    (?P<cross_1> {CROSS_1} \s* ({OPEN})? (?P<sex_1>{SEX} ) ({CLOSE})? )
    \s* ( {CONJ} | {PREP} )? \s*
    (?P<cross_2> {CROSS_2} \s* ({OPEN})? (?P<sex_2>{SEX} ) ({CLOSE})? )
    """
add_frag('sex_cross', SEX_CROSS)

# Like "to 10 cm"
CROSS_UPPER = fr"""
    ( up \s+ )? to \s+ (?P<high_length_upper> {NUMBER} ) \s+
        (?P<units_length_upper> {UNITS} ) 
    """
add_key('cross_upper', CROSS_UPPER)


add_key('count_upper', fr"""
    ( up \s+ )? to \s+ (?P<high> {NUMBER} ) 
""")

CROSS_DIM = fr"""
    ( {CROSS_UPPER} | {CROSS} ) ( \s+ (?P<dimension> {DIM}) \b )? """
add_frag('cross_dim', CROSS_DIM)


# ############################################################################

def split_keywords(value):
    """Convert a keyword string into separate keywords."""
    return re.split(fr"""
        \s* \b (?:{CONJ} | {PREP}) \b \s* [,]? \s* | \s* [,\[\]] \s*
        """, value, flags=util.FLAGS)


def set_size_values(trait, token):
    """Update the size measurements with normalized values."""
    units, multiplier = {}, {}

    if token.groups.get('high_length_upper'):
        token.groups['high_length'] = token.groups['high_length_upper']

    if token.groups.get('units_length_upper'):
        token.groups['units_length'] = token.groups['units_length_upper']

    units['length'] = token.groups.get('units_length', '').lower()
    units['width'] = token.groups.get('units_width', '').lower()

    # No units means it's not a measurement
    if not (units['length'] or units['width']):
        return False

    if not units['length']:
        multiplier['width'] = 10.0 if units['width'] == 'cm' else 1.0
        multiplier['length'] = multiplier['width']
    elif not units['width']:
        multiplier['length'] = 10.0 if units['length'] == 'cm' else 1.0
        multiplier['width'] = multiplier['length']
    else:
        multiplier['length'] = 10.0 if units['length'] == 'cm' else 1.0
        multiplier['width'] = 10.0 if units['width'] == 'cm' else 1.0

    for dimension in ['length', 'width']:
        for value in ['min', 'low', 'high', 'max']:
            key = f'{value}_{dimension}'
            if key in token.groups:
                setattr(trait, key,
                        float(token.groups[key]) * multiplier[dimension])
    return True


def part_phrase(leaf_part):
    """Build a replacer rule for the leaf part."""
    return replacer(f'{leaf_part}_phrase', f"""
        ( location ( word | punct )* )?
        (?P<part> {leaf_part} )
        """)
