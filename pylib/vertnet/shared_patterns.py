"""Shared token patterns."""

import pylib.shared.patterns as patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog, LAST
from pylib.vertnet.util import ordinal, number_to_words

CATALOG = RuleCatalog(patterns.CATALOG)

_ = CATALOG.term('word', r' ( [a-z] \w* ) ', capture=False, when=LAST)

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

CATALOG.part('shorthand_key', r"""
    (on \s* tag | specimens? (?! \s* [a-z] )
        | catalog (?! [a-z] )) (?! \s* [#] )
    | ( measurement s? | meas ) [:.,]{0,2} ( \s* length \s* )?
        (
            \s* [({\[})]?
                (t [o.]? l [._]? (?! [a-z.] )
                | [a-z]{1,2}) [)}\]]? \.?
        )?
    | tag \s+ \d+ \s* =? ( male | female)? \s* ,
    | measurements? | mesurements? | measurementsnt
    """)

# A possibly unknown value
SH_NUM = r""" \d+ ( \. \d+ )? | (?<= [^\d] ) \. \d+ """
CATALOG.part('sh_num', SH_NUM)

SH_VAL = f' ( {SH_NUM} | [?x]{{1,2}} | n/?d ) '
CATALOG.part('sh_val', SH_VAL)

CATALOG.part('shorthand', fr"""
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
        (?P<shorthand_wt_units> {patterns.METRIC_MASS} )?
        \s*? \]?
    )?
    (?! [\d/:=a-z-] )
    """)

# Sometimes the last number is missing. Be careful to not pick up dates.
CATALOG.part('triple', fr"""
    (?<! [\d/a-z-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {SH_VAL} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {SH_VAL} \]? )
    (?! [\d/:=a-z-] )
    """)

# Some numeric values are reported as ordinals or words
ORDINALS = [ordinal(x) for x in range(1, 9)]
ORDINALS += [number_to_words(x) for x in ORDINALS]
CATALOG.part('ordinals', ORDINALS)

# Time units
CATALOG.part('time_units', ' years? months? weeks? days? hours? '.split())

# Side keywords
CATALOG.part('side', r"""
    (?<! [a-z] ) [lr] (?! [a-z] )
    | both | left | right | lft? | lt | rt """)
# SIDE = RULE['side'].pattern

DIMENSION = r' (?P<dim> length | width ) '
CATALOG.part('dimension', DIMENSION)

# Numeric sides interfere with number parsing so combine \w dimension
CATALOG.part(
    'dim_side',
    fr""" {DIMENSION} \s* (?P<side> [12] ) \b """)

CATALOG.part('cyst', r"""
    (\d+ \s+)? (cyst s? | bodies | cancerous | cancer ) ( \s+ ( on | in ))?""")

# Numbers are positive decimals and estimated values are enclosed in brackets
CATALOG.part('number', r"""
    (?P<estimated_value> \[ )?
    ( ( \d{1,3} ( , \d{3} ){1,3} | \d+ ) ( \. \d+ )?
        | (?<= [^\d] ) \. \d+ | ^ \. \d+ )
    \]?
    """)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
# CATALOG.grouper('range', """
#     (?<! dash )
#     ( number units? (( dash | to ) number units?)? )
#     (?! dash ) """, capture=False)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
CATALOG.grouper('mass_range', """
    (?<! dash )
    ( number mass_units? (( dash | to ) number mass_units?)? )
    (?! dash ) """, capture=False)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
CATALOG.grouper('len_range', """
    (?<! dash )
    ( number (?P<units> len_units )?
    (( dash | to ) number (?P<units> len_units )? )? )
    (?! dash ) """, capture=False)

# A rule for parsing a compound weight like 2 lbs. 3.1 - 4.5 oz
CATALOG.grouper('compound_len', """
    (?P<ft> number ) feet comma?
    (?P<in> number ) ( ( dash | to ) (?P<in> number ) )? inches
    """, capture=False)

# A rule for parsing a compound weight like 2 lbs. 3.1 - 4.5 oz
CATALOG.grouper('compound_wt', """
    (?P<lbs> number ) pounds comma?
    (?P<ozs> number ) ( ( dash | to ) (?P<ozs> number ) )? ounces
    """, capture=False)

# A number times another number like: "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we only take
# the first two numbers
CROSS = """ (?<! x )
        ( number len_units? ( x | by ) number len_units?
        | number len_units ) """
CATALOG.grouper('cross', CROSS, capture=False)

# Handle 2 cross measurements, one per left/right side
CATALOG.grouper('joiner', ' ampersand comma and '.split())

CATALOG.grouper('side_cross', f"""
    (?P<side_1> side )?
        (?P<value_1> number ) (?P<units_1> len_units )?
            ( x | by ) (?P<value_1> number ) (?P<units_1> len_units )?
    joiner?
    (?P<side_2> side )?
        (?P<value_2> number ) (?P<units_2> len_units )?
            ( x | by ) (?P<value_2> number ) (?P<units_2> len_units )?
    """, capture=False)

# For fractions like "1 2/3" or "1/2".
# We don't allow dates like "1/2/34".
CATALOG.grouper('len_fraction', """
    (?P<whole> number )?
    (?<! slash )
    (?P<numerator> number) slash (?P<denominator> number)
    (?! slash ) (?P<units> len_units)? """, capture=False)
