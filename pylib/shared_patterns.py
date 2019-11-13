"""Shared token patterns."""

import re
from pylib.util import ordinal, number_to_words
from stacked_regex.rule import Rule, fragment


SHARED = {}


def add(rule: Rule) -> None:
    """Add a rule to SHARED."""
    SHARED[rule.name] = rule


add(fragment('feet', r" foot s? | feet s? | ft s? (?! [,\w]) | (?<= \d ) ' "))

# NOTE: Double quotes as inches is handled during fix up
# The negative look-ahead is trying to distinguish between cases like
# inTL with other words.
add(fragment('inches', ' ( inch e? s? | in s? ) (?! [a-dgi-km-ru-z] ) '))

add(fragment(
    'metric_len', r' ( milli | centi )? meters? | ( [cm] [\s.]? m ) '))

add(fragment(
    'len_units', '|'.join(
        [SHARED[x].pattern for x in ('metric_len', 'feet', 'inches')])))
LEN_UNITS = SHARED['len_units'].pattern

add(fragment('pounds', r' pounds? | lbs? '))
add(fragment('ounces', r' ounces? | ozs? '))
add(fragment('metric_mass', r"""
    ( milligram | kilogram | gram ) ( s (?! [a-z]) )?
    | ( m \.? g | k \.? \s? g | g[mr]? )
        ( s (?! [a-z]) )?
    """))

add(fragment('us_mass', '|'.join([
    SHARED[x].pattern for x in ('pounds', 'ounces')])))

add(fragment(
    'mass_units', '|'.join([
        SHARED[x].pattern for x in ('metric_mass', 'pounds', 'ounces')])))
MASS_UNITS = SHARED['mass_units'].pattern

# Numbers are positive decimals
add(fragment('number', r"""
    ( \d{1,3} ( , \d{3} ){1,3} | \d+ ) ( \. \d+ )?
    | (?<= [^\d] ) \. \d+ | ^ \. \d+
    """))
NUMBER = SHARED['number'].pattern

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
RANGE_JOINER = r'- | to'
add(fragment('range_joiner', RANGE_JOINER))
add(fragment('range', fr"""
    (?<! \d ) (?<! \d [|,.#+-] ) (?<! \b to \s ) (?<! [#] )
    (?P<estimated_value> \[ \s* )?
    (?P<value1> {NUMBER} )
    \]? \s*?
    ( \s* ( {RANGE_JOINER} ) \s* (?P<value2> {NUMBER} ) )?
    (?! \d+ | [|,.+-] \d | \s+ to \b )
    """))

# A number times another number like: "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we ony take
# the first two numbers
CROSS_JOINER = r' ( x | by | \* | - ) '
add(fragment('cross_joiner', CROSS_JOINER))
add(fragment('cross', fr"""
    (?<! [\d/,.-]\d ) (?<! \b by )
    (?P<estimated_value> \[ \s* )?
    (?P<value1> {NUMBER} ) \s*
    \]? \s*?
    ( (?P<units1a> {LEN_UNITS})
            \s* {CROSS_JOINER}
            \s* (?P<value2a> {NUMBER}) \s* (?P<units2> {LEN_UNITS})
        | {CROSS_JOINER}
            \s* (?P<value2b> {NUMBER}) \s* (?P<units1b> {LEN_UNITS})
        | {CROSS_JOINER}
            \s* (?P<value2c> {NUMBER}) \b (?! {MASS_UNITS})
        | (?P<units1c> {LEN_UNITS})
        | \b (?! {MASS_UNITS})
    )"""))
CROSS = SHARED['cross'].pattern

# For fractions like "1 2/3" or "1/2".
# We don't allow dates like "1/2/34".
add(fragment('fraction', r"""
    (?<! [\d/,.] )
    (?P<whole> \d+ \s+ )? (?P<numerator> \d+ ) / (?P<denominator> \d+ )
    (?! [\d/,.] )
    """))

# This is a common notation: "11-22-33-44:99g".
# There are other separators "/", ":", etc.
# There is also an extended form that looks like:
#   "11-22-33-44-fa55-hb66:99g" There may be several extended numbers.
#
#   11 = total length (ToL or TL) or sometimes head body length
#   22 = tail length (TaL)
#   33 = hind foot length (HFL)
#   44 = ear length (EL)
#   99 = body mass is optional, as is the mass units
#
# Unknown values are filled with "?" or "x".
#   E.g.: "11-x-x-44" or "11-?-33-44"
#
# Ambiguous measurements are enclosed in brackets.
#   E.g.: 11-[22]-33-[44]:99g

add(fragment('shorthand_key', r"""
    on \s* tag | specimens? | catalog
    | ( measurement s? | meas ) [:.,]{0,2} ( \s* length \s* )?
        ( \s* [({\[})]? [a-z]{1,2} [)}\]]? \.? )?
    | tag \s+ \d+ \s* =? ( male | female)? \s* ,
    | measurements? | mesurements? | measurementsnt
    """))

# A possibly unknown value
add(fragment('sh_num', r""" \d+ ( \. \d+ )? | (?<= [^\d] ) \. \d+ """))
SH_NUM = SHARED['sh_num'].pattern

add(fragment('sh_val', f' ( {SH_NUM} | [?x]{{1,2}} | n/?d ) '))
SH_VAL = SHARED['sh_val'].pattern

add(fragment('shorthand', fr"""
    (?<! [\d/a-z-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {SH_VAL} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_el> (?P<estimated_el> \[ )? {SH_VAL} \]? )
    (?P<shorthand_ext> ( (?P=shorthand_sep) [a-z]{{1,4}} {SH_VAL} )* )
    ( [\s=:/-] \s*
        (?P<estimated_wt> \[? \s* )
        (?P<shorthand_wt> {SH_VAL} ) \s*
        \]?
        (?P<shorthand_wt_units> {SHARED['metric_mass'].pattern} )?
        \s*? \]?
    )?
    (?! [\d/:=a-z-] )
    """))

# Sometimes the last number is missing. Be careful to not pick up dates.
add(fragment('triple', fr"""
    (?<! [\d/a-z-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {SH_VAL} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {SH_VAL} \]? )
    (?! [\d/:=a-z-] )
    """))

# UUIDs cause problems when extracting certain shorthand notations.
add(fragment('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """))

# Some numeric values are reported as ordinals or words
ORDINALS = [ordinal(x) for x in range(1, 6)]
ORDINALS += [number_to_words(x) for x in ORDINALS]
add(fragment('ordinals', ' | '.join(ORDINALS)))

# Time units
add(fragment('time_units', r'years? | months? | weeks? | days? | hours?'))

# Side keywords
add(fragment('side', r"""
    [/(\[] \s* (?P<side1> [lr] \b ) \s* [)\]]?
    | (?P<side2> both | left | right | lft | rt | [lr] \b ) """))
SIDE = SHARED['side'].pattern

add(fragment('dimension', r' (?P<dim> length | width ) '))

# Numeric sides interfere with number parsing so combine \w dimension
add(fragment(
    'dim_side',
    fr""" {SHARED['dimension'].pattern} \s* (?P<side> [12] ) \b """))

add(fragment(
    'cyst',
    r""" (\d+ \s+)?
        (cyst s? | bodies | cancerous | cancer )
        ( \s+ ( on | in ))?"""))

# integers, no commas or signs and typically small
add(fragment('integer', r""" \d+ (?! [%\d\-] ) """))

# Handle 2 cross measurements, one per left/right side
CROSS_GROUPS = re.compile(
    r"""( estimated_value | value[12][abc]? | units[12][abc]? | side[12] ) """,
    re.IGNORECASE | re.VERBOSE)
CROSS_1 = CROSS_GROUPS.sub(r'\1_1', CROSS)
CROSS_2 = CROSS_GROUPS.sub(r'\1_2', CROSS)
SIDE_1 = CROSS_GROUPS.sub(r'\1_1', SIDE)
SIDE_2 = CROSS_GROUPS.sub(r'\1_2', SIDE)
SIDE_CROSS = fr"""
    (?P<cross_1> ({SIDE_1})? \s* ({CROSS_1}) )
    \s* ( [&,] | and )? \s*
    (?P<cross_2> ({SIDE_2})? \s* ({CROSS_2}) )
    """
add(fragment('side_cross', SIDE_CROSS))
