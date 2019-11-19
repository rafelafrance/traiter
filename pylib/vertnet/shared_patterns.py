"""Shared token patterns."""

# import regex
import pylib.shared.patterns as patterns
from pylib.shared.patterns import add_frag  # , add_rep
from pylib.vertnet.util import ordinal, number_to_words


RULE = patterns.RULE

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

add_frag('shorthand_key', r"""
    on \s* tag | specimens? | catalog
    | ( measurement s? | meas ) [:.,]{0,2} ( \s* length \s* )?
        ( \s* [({\[})]? [a-z]{1,2} [)}\]]? \.? )?
    | tag \s+ \d+ \s* =? ( male | female)? \s* ,
    | measurements? | mesurements? | measurementsnt
    """)

# A possibly unknown value
add_frag('sh_num', r""" \d+ ( \. \d+ )? | (?<= [^\d] ) \. \d+ """)
SH_NUM = RULE['sh_num'].pattern

add_frag('sh_val', f' ( {SH_NUM} | [?x]{{1,2}} | n/?d ) ')
SH_VAL = RULE['sh_val'].pattern

add_frag('shorthand', fr"""
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
add_frag('triple', fr"""
    (?<! [\d/a-z-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {SH_VAL} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {SH_VAL} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {SH_VAL} \]? )
    (?! [\d/:=a-z-] )
    """)

# UUIDs cause problems when extracting certain shorthand notations.
add_frag('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """)

# Some numeric values are reported as ordinals or words
ORDINALS = [ordinal(x) for x in range(1, 6)]
ORDINALS += [number_to_words(x) for x in ORDINALS]
add_frag('ordinals', ' | '.join(ORDINALS))

# Time units
add_frag('time_units', r'years? | months? | weeks? | days? | hours?')

# Side keywords
add_frag('side', r"""
    [/(\[] \s* (?P<side1> [lr] \b ) \s* [)\]]?
    | (?P<side2> both | left | right | lft | rt | [lr] \b ) """)
SIDE = RULE['side'].pattern

add_frag('dimension', r' (?P<dim> length | width ) ')

# Numeric sides interfere with number parsing so combine \w dimension
add_frag(
    'dim_side',
    fr""" {RULE['dimension'].pattern} \s* (?P<side> [12] ) \b """)

add_frag(
    'cyst',
    r""" (\d+ \s+)?
        (cyst s? | bodies | cancerous | cancer )
        ( \s+ ( on | in ))?""")

# Handle 2 cross measurements, one per left/right side
# CROSS_GROUPS = regex.compile(
#     r"""( estimated_value | value[12][abc]?
#           | units[12][abc]? | side[12] ) """,
#     regex.IGNORECASE | regex.VERBOSE)
# CROSS_1 = CROSS_GROUPS.sub(r'\1_1', CROSS)
# CROSS_2 = CROSS_GROUPS.sub(r'\1_2', CROSS)
# SIDE_1 = CROSS_GROUPS.sub(r'\1_1', SIDE)
# SIDE_2 = CROSS_GROUPS.sub(r'\1_2', SIDE)
# SIDE_CROSS = fr"""
#     (?P<cross_1> ({SIDE_1})? \s* ({CROSS_1}) )
#     \s* ( [&,] | and )? \s*
#     (?P<cross_2> ({SIDE_2})? \s* ({CROSS_2}) )
#     """
# add_frag('side_cross', SIDE_CROSS)
