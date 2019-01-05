"""Shared parser patterns."""

# pylint: disable=invalid-name

import re
import string
from pyparsing import punc8bit, Regex


flags = re.VERBOSE | re.IGNORECASE
punct = string.punctuation + punc8bit


number_re = r' (?: (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? ) '


def boundary(regexp, left=True, right=True):
    r"""Wrap a regular expression in \b character class."""
    left = r'\b' if left else ''
    right = r'\b' if right else ''
    return r'{} (?: {} ) {}'.format(left, regexp, right)


# Numbers are positive decimals
number = Regex(number_re, flags)

# A number or a pair of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a pair
pair_joiner = r'- | to'
pair = Regex(r"""
    (?<! \d ) (?<! \d [/,.-] ) (?<! \b to )
    (?P<value1> {val} ) (?: \s* (?: {joiner} ) \s* (?P<value2> {val} ) )?
    (?! [/,.-] \d ) (?! \d+ ) (?! \s+ to )
    """.format(val=number_re, joiner=pair_joiner), flags)

# A number times another number like "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we ony take the
# first two numbers
cross_joiner = r'x | by | \*'
cross = Regex(r"""
    (?<! [\d/,.-] \d ) (?<! \b by ) (?<! \* ) (?<! x )
    (?P<value1> {val} ) (?: \s* (?: {joiner} ) \s* (?P<value2> {val} ) )?
    """.format(val=number_re, joiner=cross_joiner), flags)

# For fractions like "1 2/3" or "1/2".
# We don't allow date like "1/2/34". No part of this is a fraction
fraction_joiner = '/'
fraction = Regex(r"""
    (?<! [\d/] )
    (?: (?P<whole> \d+ ) \s+ )?
    (?P<numerator> \d+ ) (?: {joiner} ) (?P<denominator> \d+ )
    (?! [\d/] )
    """.format(joiner=fraction_joiner), flags)

feet = Regex(r' (?: foot | feet | ft ) s? ', flags)

inches = Regex(r' (?: inch e? | in ) s? ', flags)

metric_len = Regex(r"""
    millimeters? | centimeters? | meters? | (?: [cm] [\s.]? m )
    """, flags)

len_units = (metric_len | feet | inches)('units')

pounds = Regex(r' (?: pound | lb ) s? ', flags)

ounces = Regex(r' (?: ounce | oz ) s? ', flags)

metric_mass_re = r"""
    (?: milligram | kilogram | gram ) (?: s (?! [a-z]) )?
    | (?: m \.? g | k \.? g | g[mr]? ) (?: s (?! [a-z]) )?
    """
metric_mass = Regex(metric_mass_re, flags)

mass_units = (metric_mass | pounds | ounces)('units')

shorthand_key = Regex(r"""
    on \s* tag | specimens? | catalog
    | meas (?: urements )? [:.,]{0,2} (?: \s* length \s* )?
        (?: \s* [({\[})]? [a-z]{1,2} [)}\]]? \.? )?
    | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
    | mesurements | Measurementsnt
    """, flags)

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
# Unknown values are filled with "?" or "x".
#   Like "11-x-x-44" or "11-?-33-44"
# Ambiguous measurements are enclosed in brackets.
#   Like 11-[22]-33-[44]:99g

sh_val = r' {number} | [?x]{repeat} | \[{number}\] | \[[?x]{repeat}\]'.format(
    number=number_re, repeat='{1,2}')
shorthand = Regex(r"""
    (?<! [\d/-] )
    (?P<shorthand_tl> {sh_val} )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> {sh_val} )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> {sh_val} )
    (?P=shorthand_sep)
    (?P<shorthand_eal> {sh_val} )
    (?P<shorthand_ext> (?: (?P=shorthand_sep) [a-z]{repeat14} {sh_val} )* )
    (?: [\s=:/-] \s*
        (?P<shorthand_wt> {sh_val} ) \s*
        (?P<shorthand_wt_units> {units} )? )?
    (?! [\d/:=-] )
    """.format(sh_val=sh_val, repeat14='{1,4}', units=metric_mass_re), flags)
