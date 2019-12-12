"""Shared token patterns."""

import pylib.shared.patterns as patterns
from pylib.shared.rule_set import RuleSet
from pylib.vertnet.util import ordinal, number_to_words

SET = RuleSet(patterns.SET)
RULE = SET.rules


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

SET.add_frag('shorthand_key', r"""
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
SET.add_frag('sh_num', r""" \d+ ( \. \d+ )? | (?<= [^\d] ) \. \d+ """)
SH_NUM = RULE['sh_num'].pattern

SET.add_frag('sh_val', f' ( {SH_NUM} | [?x]{{1,2}} | n/?d ) ')
SH_VAL = RULE['sh_val'].pattern

SET.add_frag('shorthand', fr"""
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
SET.add_frag('triple', fr"""
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
SET.add_frag('ordinals', ORDINALS)

# Time units
SET.add_frag('time_units', ' years? months? weeks? days? hours? '.split())

# Side keywords
SET.add_frag('side', r"""
    (?<! [a-z] ) [lr] (?! [a-z] )
    | both | left | right | lft? | lt | rt """)
# SIDE = RULE['side'].pattern

SET.add_frag('dimension', r' (?P<dim> length | width ) ')

# Numeric sides interfere with number parsing so combine \w dimension
SET.add_frag(
    'dim_side',
    fr""" {RULE['dimension'].pattern} \s* (?P<side> [12] ) \b """)

SET.add_frag('cyst', r"""
    (\d+ \s+)? (cyst s? | bodies | cancerous | cancer ) ( \s+ ( on | in ))?""")

# Numbers are positive decimals and estimated values are enclosed in brackets
SET.add_frag('number', r"""
    (?P<estimated_value> \[ )?
    ( ( \d{1,3} ( , \d{3} ){1,3} | \d+ ) ( \. \d+ )?
        | (?<= [^\d] ) \. \d+ | ^ \. \d+ )
    \]?
    """)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
SET.add_group('range', """
    (?<! dash )
    ( number units? (( dash | to ) number units?)? )
    (?! dash ) """, capture=False)
# Rule set for parsing a range
SET.add_set('range_set', [
    RULE['inches'],
    RULE['feet'],
    RULE['metric_len'],
    RULE['len_units'],
    RULE['pounds'],
    RULE['ounces'],
    RULE['metric_mass'],
    RULE['mass_units'],
    RULE['units'],
    RULE['number'],
    RULE['dash'],
    RULE['to'],
    RULE['range'],
])

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
SET.add_group('len_range', """
    (?<! dash )
    ( number (?P<units> len_units )?
    (( dash | to ) number (?P<units> len_units )? )? )
    (?! dash ) """, capture=False)
# Rule set for parsing a range
SET.add_set('len_range_set', [
    RULE['inches'],
    RULE['feet'],
    RULE['metric_len'],
    RULE['len_units'],
    RULE['number'],
    RULE['dash'],
    RULE['to'],
    RULE['len_range'],
])

# A rule for parsing a compound weight like 2 lbs. 3.1 - 4.5 oz
SET.add_group('compound_len', """
    (?P<ft> number ) feet comma?
    (?P<in> number ) ( ( dash | to ) (?P<in> number ) )? inches
    """, capture=False)
# Rule set for parsing a compound_wt
SET.add_set('compound_len_set', [
    RULE['feet'],
    RULE['inches'],
    RULE['number'],
    RULE['dash'],
    RULE['comma'],
    RULE['to'],
    RULE['compound_len'],
])

# A rule for parsing a compound weight like 2 lbs. 3.1 - 4.5 oz
SET.add_group('compound_wt', """
    (?P<lbs> number ) pounds comma?
    (?P<ozs> number ) ( ( dash | to ) (?P<ozs> number ) )? ounces
    """, capture=False)
# Rule set for parsing a compound_wt
SET.add_set('compound_wt_set', [
    RULE['pounds'],
    RULE['ounces'],
    RULE['number'],
    RULE['dash'],
    RULE['comma'],
    RULE['to'],
    RULE['compound_wt'],
])

# A number times another number like: "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we only take
# the first two numbers
CROSS = """ (?<! x )
        ( number len_units? ( x | by ) number len_units?
        | number len_units ) """
SET.add_group('cross', CROSS, capture=False)
# Rule set for parsing a cross
SET.add_set('cross_set', [
    RULE['inches'],
    RULE['feet'],
    RULE['metric_len'],
    RULE['len_units'],
    RULE['number'],
    RULE['x'],
    RULE['by'],
    RULE['cross'],
])

# Handle 2 cross measurements, one per left/right side
SET.add_group('joiner', ' ampersand comma and '.split())

SET.add_group('side_cross', f"""
    (?P<side_1> side )?
        (?P<value_1> number ) (?P<units_1> len_units )?
            ( x | by ) (?P<value_1> number ) (?P<units_1> len_units )?
    joiner?
    (?P<side_2> side )?
        (?P<value_2> number ) (?P<units_2> len_units )?
            ( x | by ) (?P<value_2> number ) (?P<units_2> len_units )?
    """, capture=False)
SET.add_set('side_cross_set', [
    RULE['inches'],
    RULE['feet'],
    RULE['metric_len'],
    RULE['len_units'],
    RULE['number'],
    RULE['x'],
    RULE['ampersand'],
    RULE['comma'],
    RULE['and'],
    RULE['by'],
    RULE['joiner'],
    RULE['side'],
    RULE['side_cross'],
])

# For fractions like "1 2/3" or "1/2".
# We don't allow dates like "1/2/34".
SET.add_group('fraction', """
    (?P<whole> number )?
    (?<! slash )
    (?P<numerator> number) slash (?P<denominator> number)
    (?! slash ) units? """, capture=False)
# Rule set for parsing fractions
SET.add_set('fraction_set', [
    RULE['inches'],
    RULE['feet'],
    RULE['metric_len'],
    RULE['len_units'],
    RULE['pounds'],
    RULE['ounces'],
    RULE['metric_mass'],
    RULE['mass_units'],
    RULE['units'],
    RULE['number'],
    RULE['slash'],
    RULE['fraction'],
])

# For fractions like "1 2/3" or "1/2".
# We don't allow dates like "1/2/34".
SET.add_group('len_fraction', """
    (?P<whole> number )?
    (?<! slash )
    (?P<numerator> number) slash (?P<denominator> number)
    (?! slash ) (?P<units> len_units)? """, capture=False)
# Rule set for parsing fractions
SET.add_set('len_fraction_set', [
    RULE['inches'],
    RULE['feet'],
    RULE['metric_len'],
    RULE['len_units'],
    RULE['number'],
    RULE['slash'],
    RULE['len_fraction'],
])
