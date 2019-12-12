"""Shared plant parser logic."""

import regex
import pylib.shared.patterns as patterns
from pylib.shared.rule_set import RuleSet


SET = RuleSet(patterns.SET)
RULE = SET.rules


SET.add_key('sex', 'staminate pistillate'.split())

SET.add_key('plant_part', r"""
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

SET.add_key('leaf', r""" leaf (\s* blades?)? | leaflet | leaves | blades? """)
SET.add_key('petiole', r""" (?<! to \s ) (petioles? | petiolules?)""")
SET.add_key('lobes', r' ( leaf \s* )? (un)?lobe[sd]? ')
SET.add_key('hairs', 'hairs?')
SET.add_key('flower', fr'({RULE["sex"].regexp.pattern} \s+ )? flowers?')
SET.add_key('hypanthium', 'hypan-?thi(um|a)')
SET.add_key('sepal', 'sepals?')
SET.add_key('calyx', 'calyx | calyces')
SET.add_key('stamen', 'stamens?')
SET.add_key('anther', 'anthers?')
SET.add_key('style', 'styles?')
SET.add_key('stigma', 'stigmas?')
SET.add_key('petal', r' petals? ')
SET.add_key('corolla', r' corollas? ')

SET.add_key('shape_starter', """
    broadly
    deeply depressed
    long
    mostly
    narrowly nearly
    partly
    shallowly sometimes
    """.split())

SET.add_frag('location', r""" \b ( terminal | lateral | basal | cauline ) """)
SET.add_key('dim', """
    width wide length long radius diameter diam? """.split())

SET.add_frag('punct', r' [,;:/] ', capture=False)

SET.add_key('word', r' [a-z] \w* ', capture=False)


# ############################################################################
# Numeric patterns

SET.add_key('units', ' cm mm '.split())

SET.add_frag('number', r' \d+ ( \. \d* )? ')


# Numeric ranges like: (10–)15–20(–25)
SET.add_group('range', r"""
    (?<! slash | dash | number )
    (?: open (?P<min> number ) dash close )?
    (?P<low> number )
    (?: dash (?P<high> number ) )?
    (?: open dash (?P<max> number ) close )?
    (?! dash | slash )
    """, capture=False)

SET.add_set('range_set', [
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

SET.add_group('cross', f"""
    {LENGTH_RANGE} (?P<units_length> units )?
    ( x {WIDTH_RANGE} (?P<units_width> units )? )?
    """, capture=False)
SET.add_set('cross_set', [
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
SET.add_group('sex_cross', f"""
    {CROSS_1} (open)? (?P<sex_1> sex )? (close)?
    ( conj | prep )?
    {CROSS_2} (open)? (?P<sex_2> sex )? (close)?
    """, capture=False)
SET.add_set('sex_cross_set', [
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
SET.add_group(
    'cross_upper',
    fr""" up_to (?P<high_length> number )
        (?P<units_length> units ) """, capture=False)
SET.add_set('cross_upper_set', [
    RULE['up_to'],
    RULE['units'],
    RULE['number'],
    RULE['cross_upper']])

# Like "to 10"
SET.add_group('count_upper', fr""" up_to (?P<high> number ) """, capture=False)
SET.add_set('count_upper_set', [
    RULE['up_to'],
    RULE['number'],
    RULE['count_upper']])
