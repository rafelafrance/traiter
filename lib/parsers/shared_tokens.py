"""Shared token patterns."""

# pylint: disable=invalid-name


feet = ('feet', r" foots? | feets? | fts? | (?<= \d ) ' ")

# NOTE: Double quotes as inches is handled during fix up
inches = ('inches', ' inche?s? | ins? ')

metric_len = (
    'metric_len', r'(?: milli | centi )? meters? | (?: [cm] [\s.]? m ) ')

len_units = ('len_units', '|'.join([x[1] for x in (metric_len, feet, inches)]))

pounds = (' pounds', r' pounds? | lbs? ')

ounces = (' ounces', r' ounces? | ozs? ')

metric_mass = ('metric_mass', r"""
    (?: milligram | kilogram | gram ) (?: s (?! [a-z]) )?
    | (?: m \.? g | k \.? g | g[mr]? ) (?: s (?! [a-z]) )?
    """)

mass_units = (
    'mass_units', '|'.join([x[1] for x in (metric_mass, pounds, ounces)]))

# Numbers are positive decimals
number = ('number', r' (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? ')

# A number or a pair of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a pair
pair_joiner = r'- | to'
pair = ('pair', fr"""
    (?<! \d ) (?<! \d [|,.-] ) (?<! \b to \s )
    (?P<value1> {number[1]} )
        (?: \s* (?: {pair_joiner} ) \s* (?P<value2> {number[1]} ) )?
    (?! \d+ | [|,.-] \d | \s+ to \b )
    """)

# A number times another number like: "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we ony take the
# first two numbers
cross_joiner = r' (?: x | by | \* | - ) '
cross = ('cross', fr"""
    (?<! [\d/,.-]\d ) (?<! \b by )
    (?P<value1> {number[1]} ) \s* (?P<units1> {len_units[1]} )
        \s* {cross_joiner}
        \s* (?P<value2> {number[1]} ) \s* (?P<units2> {len_units[1]} )
    | (?P<value1> {number[1]} )
        (?: \s* (?: {cross_joiner} ) \s* (?P<value2> {number[1]} ) )?
        (?: \s* (?P<units1> {len_units[1]} ))?
    """)

# For fractions like "1 2/3" or "1/2".
# We don't allow date like "1/2/34". No part of this is a fraction
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
#   Like: "11-x-x-44" or "11-?-33-44"
#
# Ambiguous measurements are enclosed in brackets.
#   Like: 11-[22]-33-[44]:99g

shorthand_key = ('shorthand_key', r"""
    on \s* tag | specimens? | catalog
    | meas (?: urements? )? [:.,]{0,2} (?: \s* length \s* )?
        (?: \s* [({\[})]? [a-z]{1,2} [)}\]]? \.? )?
    | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
    | measurements? | mesurements? | Measurementsnt
    """)

# A possibly unknown value
sh_val = ('sh_val', f' (?: {number[1]} | [?x]{{1,2}} ) ')

shorthand = ('shorthand', fr"""
    (?<! [\d/-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {sh_val[1]} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {sh_val[1]} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {sh_val[1]} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_el> (?P<estimated_el> \[ )? {sh_val[1]} \]? )
    (?P<shorthand_ext> (?: (?P=shorthand_sep) [a-z]{{1,4}} {sh_val[1]} )* )
    (?: [\s=:/-] \s*
        (?P<estimated_wt> \[? \s* )
        (?P<shorthand_wt> {sh_val[1]} ) \s*
        \]?
        (?P<shorthand_wt_units> {metric_mass[1]} )?
        \s*? \]?
    )?
    (?! [\d/:=-] )
    """)

# Apparently, they sometimes don't fill in the last number. We have to be extra
# careful using this pattern so we don't pick up dates. Surround this token
# with keys and lookarounds.
triple = ('triple', fr"""
    (?<! [\d/-] )
    (?P<shorthand_tl> (?P<estimated_tl> \[ )? {sh_val[1]} \]? )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> (?P<estimated_tal> \[ )? {sh_val[1]} \]? )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> (?P<estimated_hfl> \[ )? {sh_val[1]} \]? )
    (?! [\d/:=-] )
    """)
