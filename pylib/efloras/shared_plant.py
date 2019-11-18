"""Shared plant parser logic."""

import re
from pylib.stacked_regex.rule import Rule, fragment, keyword, replacer
import pylib.efloras.util as util


SCANNER = {}


def add(rule: Rule) -> None:
    """Add a rule to SCANNER."""
    SCANNER[rule.name] = rule


SEX = 'staminate | pistillate'
add(keyword('sex', SEX))

CONJ = ' or | and '
add(keyword('conj', CONJ))
PREP = ' to | with '
add(keyword('prep', PREP))

add(keyword('plant_part', r"""
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
    """))

add(keyword('leaf', r""" leaf (\s* blades?)? | leaflet | leaves | blades? """))
add(keyword(
    'petiole', r""" (?<! to \s ) (petioles? | petiolules?)"""))
add(keyword('lobes', r' ( leaf \s* )? (un)?lobe[sd]? '))
add(keyword('hairs', 'hairs?'))
add(keyword('flower', fr'({SCANNER["sex"].regex.pattern} \s+ )? flowers?'))
add(keyword('hypanthium', 'hypan-?thi(um|a)'))
add(keyword('sepal', 'sepals?'))
add(keyword('calyx', 'calyx | calyces'))
add(keyword('stamen', 'stamens?'))
add(keyword('anther', 'anthers?'))
add(keyword('style', 'styles?'))
add(keyword('stigma', 'stigmas?'))
add(keyword('petal', r' petals? '))
add(keyword('corolla', r' corollas? '))

add(keyword('shape_starter', r"""
    broadly
    deeply depressed 
    long
    mostly
    narrowly nearly
    partly
    shallowly sometimes
    """.split()))

add(fragment('location', r""" \b ( terminal | lateral | basal | cauline ) """))

add(fragment('punct', r' [,;:/] '))

DIM = """ width | wide | length | long | radius | diameter | diam? """
add(keyword('dim', DIM))
add(keyword('word', r' [a-z] \w* '))


# ############################################################################
# Numeric patterns

UNITS = r' cm | mm '
add(keyword('units', UNITS))

NUMBER = r' \d+ ( \. \d* )? '
add(fragment('number', NUMBER))

DASH = r' (?: – | - ) '
add(fragment('dash', DASH))

OPEN = r' [(\[] '
CLOSE = r' [)\]] '
add(fragment('open', OPEN))
add(fragment('close', CLOSE))

# Numeric ranges like: (10–)15–20(–25)
RANGE = fr"""
    (?<! [/\d\-] )
    (?: {OPEN} \s* (?P<min> {NUMBER} ) \s* {DASH} \s* {CLOSE} \s* )?
    (?P<low> {NUMBER} )
    (?: \s* {DASH} \s* (?P<high> {NUMBER} ) )?
    (?: \s* {OPEN} \s* {DASH} \s* (?P<max> {NUMBER} ) \s* {CLOSE} )?
    """
add(fragment('range', RANGE))

# Cross measurements like: 3–5(–8) × 4–11(–13)
CROSS_JOINER = r' x | × '
add(fragment('cross_joiner', CROSS_JOINER))

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
add(fragment('cross', CROSS))

CROSS_GROUPS = re.compile(
    r""" (length | width) """, re.IGNORECASE | re.VERBOSE)
CROSS_1 = CROSS_GROUPS.sub(r'\1_1', CROSS)
CROSS_2 = CROSS_GROUPS.sub(r'\1_2', CROSS)
SEX_CROSS = fr"""
    (?P<cross_1> {CROSS_1} \s* ({OPEN})? (?P<sex_1>{SEX} ) ({CLOSE})? )
    \s* ( {CONJ} | {PREP} )? \s*
    (?P<cross_2> {CROSS_2} \s* ({OPEN})? (?P<sex_2>{SEX} ) ({CLOSE})? )
    """
add(fragment('sex_cross', SEX_CROSS))

# Like "to 10 cm"
CROSS_UPPER = fr"""
    ( up \s+ )? to \s+ (?P<high_length_upper> {NUMBER} ) \s+
        (?P<units_length_upper> {UNITS} ) 
    """
add(keyword('cross_upper', CROSS_UPPER))


add(keyword('count_upper', fr"""
    ( up \s+ )? to \s+ (?P<high> {NUMBER} ) 
"""))

CROSS_DIM = fr"""
    ( {CROSS_UPPER} | {CROSS} ) ( \s+ (?P<dimension> {DIM}) \b )? """
add(fragment('cross_dim', CROSS_DIM))


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
