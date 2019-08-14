"""Shared token patterns."""

from lib.util import ordinal, number_to_words


feet = ('feet', r" foot s? | feet s? | ft s? | (?<= \d ) ' ")

# NOTE: Double quotes as inches is handled during fix up
# The negative look-ahead is trying to distinguish between cases like inTL
# with other words.
inches = ('inches', ' ( inch e? s? | in s? ) (?! [a-dgi-km-ru-z] ) ')

metric_len = (
    'metric_len', r' ( milli | centi )? meters? | ( [cm] [\s.]? m ) ')

len_units = ('len_units', '|'.join([x[1] for x in (metric_len, feet, inches)]))

pounds = ('pounds', r' pounds? | lbs? ')

ounces = ('ounces', r' ounces? | ozs? ')

metric_mass = ('metric_mass', r"""
    ( milligram | kilogram | gram ) ( s (?! [a-z]) )?
    | ( m \.? g | k \.? \s? g | g[mr]? )
        ( s (?! [a-z]) )?
    """)

us_mass = ('us_mass', '|'.join([x[1] for x in (pounds, ounces)]))

mass_units = (
    'mass_units', '|'.join([x[1] for x in (metric_mass, pounds, ounces)]))

# Numbers are positive decimals
number = ('number', r"""
    ( \d{1,3} ( , \d{3} ){1,3} | \d+ ) ( \. \d+ )?
    | (?<= [^\d] ) \. \d+ | ^ \. \d+
    """)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
range_joiner = r'- | to'
range_ = ('range', fr"""
    (?<! \d ) (?<! \d [|,.#+-] ) (?<! \b to \s ) (?<! [#] )
    (?P<estimated_value> \[ \s* )?
    (?P<value1> {number[1]} )
    \]? \s*?
    ( \s* ( {range_joiner} ) \s* (?P<value2> {number[1]} ) )?
    (?! \d+ | [|,.+-] \d | \s+ to \b )
    """)

# A number times another number like: "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we ony take the
# first two numbers
cross_joiner = r' ( x | by | \* | - ) '
cross = ('cross', fr"""
    (?<! [\d/,.-]\d ) (?<! \b by )
    (?P<estimated_value> \[ \s* )?
    (?P<value1> {number[1]} ) \s*
    \]? \s*?
    ( (?P<units1> {len_units[1]})
            \s* {cross_joiner}
            \s* (?P<value2> {number[1]}) \s* (?P<units2> {len_units[1]})
        | {cross_joiner}
            \s* (?P<value2> {number[1]}) \s* (?P<units1> {len_units[1]})
        | {cross_joiner}
            \s* (?P<value2> {number[1]}) \b (?! {mass_units[1]})
        | (?P<units1> {len_units[1]})
        | \b (?! {mass_units[1]})
    )""")

# For fractions like "1 2/3" or "1/2".
# We don't allow dates like "1/2/34".
fraction = ('fraction', r"""
    (?<! [\d/,.] )
    (?P<whole> \d+ \s+ )? (?P<numerator> \d+ ) / (?P<denominator> \d+ )
    (?! [\d/,.] )
    """)

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

shorthand_key = ('shorthand_key', r"""
    on \s* tag | specimens? | catalog
    | ( measurement s? | meas ) [:.,]{0,2} ( \s* length \s* )?
        ( \s* [({\[})]? [a-z]{1,2} [)}\]]? \.? )?
    | tag \s+ \d+ \s* =? ( male | female)? \s* ,
    | measurements? | mesurements? | measurementsnt
    """)

# A possibly unknown value
sh_num = ('sh_num', r""" \d+ ( \. \d+ )? | (?<= [^\d] ) \. \d+ """)
sh_val = ('sh_val', f' ( {sh_num[1]} | [?x]{{1,2}} | n/?d ) ')

shorthand = ('shorthand', fr"""
    (?<! [\d/a-z-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {sh_val[1]} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {sh_val[1]} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {sh_val[1]} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_el> (?P<estimated_el> \[ )? {sh_val[1]} \]? )
    (?P<shorthand_ext> ( (?P=shorthand_sep) [a-z]{{1,4}} {sh_val[1]} )* )
    ( [\s=:/-] \s*
        (?P<estimated_wt> \[? \s* )
        (?P<shorthand_wt> {sh_val[1]} ) \s*
        \]?
        (?P<shorthand_wt_units> {metric_mass[1]} )?
        \s*? \]?
    )?
    (?! [\d/:=a-z-] )
    """)

# Sometimes the last number is missing. Be careful to not pick up dates.
triple = ('triple', fr"""
    (?<! [\d/a-z-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {sh_val[1]} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {sh_val[1]} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {sh_val[1]} \]? )
    (?! [\d/:=a-z-] )
    """)

# UUIDs cause problems when extracting certain shorthand notations.
uuid = ('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """)

# Some numeric values are reported as ordinals or words
ordinals = [ordinal(x) for x in range(1, 6)]
ordinals += [number_to_words(x) for x in ordinals]
ordinals = ('ordinals', ' | '.join([x for x in ordinals]))


# Time units
time_units = ('time_units', r'years? | months? | weeks? | days? | hours?')


# Side keywords
side = ('side', r"""
    [/(\[] \s* (?P<side> [lr] \b ) \s* [)\]]? 
    | (?P<side> both | left | right | lft | rt | [lr] \b ) """)

# Dimension
dimension = ('dimension', r' (?P<dimension> length | width ) ')


# Numeric sides interfere with the number parsing so combine it with dimension
dim_side = ('dim_side', fr""" {dimension[1]} \s* (?P<side> [12] ) \b """)


# Cyst
cyst = ('cyst',
        r""" (\d+ \s+)?
            (cyst s? | bodies | cancerous | cancer )
            ( \s+ ( on | in ))?""")
