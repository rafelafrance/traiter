"""Shared token patterns."""

import pylib.shared.patterns as patterns
from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.util import ordinal, number_to_words

CAT = RuleCatalog(patterns.CAT)
RULE = CAT.rules


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

CAT.part('shorthand_key', r"""
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
CAT.part('sh_num', r""" \d+ ( \. \d+ )? | (?<= [^\d] ) \. \d+ """)
SH_NUM = RULE['sh_num'].pattern

CAT.part('sh_val', f' ( {SH_NUM} | [?x]{{1,2}} | n/?d ) ')
SH_VAL = RULE['sh_val'].pattern

CAT.part('shorthand', fr"""
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
        (?P<shorthand_wt_units> {RULE['metric_mass'].pattern} )?
        \s*? \]?
    )?
    (?! [\d/:=a-z-] )
    """)

# Sometimes the last number is missing. Be careful to not pick up dates.
CAT.part('triple', fr"""
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
CAT.part('ordinals', ORDINALS)

# Time units
CAT.part('time_units', ' years? months? weeks? days? hours? '.split())

# Side keywords
CAT.part('side', r"""
    (?<! [a-z] ) [lr] (?! [a-z] )
    | both | left | right | lft? | lt | rt """)
# SIDE = RULE['side'].pattern

CAT.part('dimension', r' (?P<dim> length | width ) ')

# Numeric sides interfere with number parsing so combine \w dimension
CAT.part(
    'dim_side',
    fr""" {RULE['dimension'].pattern} \s* (?P<side> [12] ) \b """)

CAT.part('cyst', r"""
    (\d+ \s+)? (cyst s? | bodies | cancerous | cancer ) ( \s+ ( on | in ))?""")

# Numbers are positive decimals and estimated values are enclosed in brackets
CAT.part('number', r"""
    (?P<estimated_value> \[ )?
    ( ( \d{1,3} ( , \d{3} ){1,3} | \d+ ) ( \. \d+ )?
        | (?<= [^\d] ) \. \d+ | ^ \. \d+ )
    \]?
    """)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
CAT.grouper('range', """
    (?<! dash )
    ( number units? (( dash | to ) number units?)? )
    (?! dash ) """, capture=False)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
CAT.grouper('len_range', """
    (?<! dash )
    ( number (?P<units> len_units )?
    (( dash | to ) number (?P<units> len_units )? )? )
    (?! dash ) """, capture=False)

# A rule for parsing a compound weight like 2 lbs. 3.1 - 4.5 oz
CAT.grouper('compound_len', """
    (?P<ft> number ) feet comma?
    (?P<in> number ) ( ( dash | to ) (?P<in> number ) )? inches
    """, capture=False)

# A rule for parsing a compound weight like 2 lbs. 3.1 - 4.5 oz
CAT.grouper('compound_wt', """
    (?P<lbs> number ) pounds comma?
    (?P<ozs> number ) ( ( dash | to ) (?P<ozs> number ) )? ounces
    """, capture=False)

# A number times another number like: "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we only take
# the first two numbers
CROSS = """ (?<! x )
        ( number len_units? ( x | by ) number len_units?
        | number len_units ) """
CAT.grouper('cross', CROSS, capture=False)


# Handle 2 cross measurements, one per left/right side
CAT.grouper('joiner', ' ampersand comma and '.split())

CAT.grouper('side_cross', f"""
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
CAT.grouper('fraction', """
    (?P<whole> number )?
    (?<! slash )
    (?P<numerator> number) slash (?P<denominator> number)
    (?! slash ) units? """, capture=False)

# For fractions like "1 2/3" or "1/2".
# We don't allow dates like "1/2/34".
CAT.grouper('len_fraction', """
    (?P<whole> number )?
    (?<! slash )
    (?P<numerator> number) slash (?P<denominator> number)
    (?! slash ) (?P<units> len_units)? """, capture=False)
