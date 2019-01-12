"""Shared parser patterns."""

# pylint: disable=invalid-name

import re
import string
from pyparsing import punc8bit, nums, Regex, Word, Keyword, ParserElement
from pyparsing import CaselessLiteral as lit

ParserElement.enablePackrat()


flags = re.VERBOSE | re.IGNORECASE
punct = string.punctuation + punc8bit


def kwd(word):
    """Workaround a bug in pyparsing CaselessKeyword."""
    return Keyword(word, caseless=True)


feet = (
    lit('foots') | lit('feets') | lit('foot') | lit('feet')
    | lit('fts') | lit('ft') | lit("'")
)

# NOTE: Double quotes as inches is being handled in the fix_up stage.
inches = (
    lit('inches') | lit('inche') | lit('inchs') | lit('inch')
    | lit('ins') | lit('in')
)

metric_len = Regex(r"""
    millimeters? | centimeters? | meters? | (?: [cm] [\s.]? m )
    """, flags)

len_units = metric_len | feet | inches

pounds = lit('pounds') | lit('pound') | lit('lbs') | lit('lb')

ounces = lit('ounces') | lit('ounce') | lit('ozs') | lit('oz')

metric_mass_re = r"""
    (?: milligram | kilogram | gram ) (?: s (?! [a-z]) )?
    | (?: m \.? g | k \.? g | g[mr]? ) (?: s (?! [a-z]) )?
    """
metric_mass = Regex(metric_mass_re, flags)

mass_units = metric_mass | pounds | ounces

# Numbers are positive decimals
number_re = r' (?: (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? ) '
number = Regex(number_re, flags)

# A number or a pair of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a pair
pair_joiner = r'- | to'
pair = Regex(fr"""
    (?<! \d ) (?<! \d [|,.-] ) (?<! \b to \s )
    (?P<value1> {number_re} )
        (?: \s* (?: {pair_joiner} ) \s* (?P<value2> {number_re} ) )?
    (?! \d+ ) (?! [|,.-] \d ) (?! \s+ to \b )
    """, flags)

# A number times another number like: "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we ony take the
# first two numbers
cross_re = r' (?: x | by | \* ) '
cross_joiner = Regex(cross_re, flags)
cross = (
    (number('value1') + len_units('units1') + cross_joiner
     + number('value2') + len_units('units2'))
    | number('value1') + cross_joiner + number('value2') + len_units('units1')
    | number('value1') + cross_joiner + number('value2')
    | number('value1') + len_units('units1')
    | number('value1')
)

# For fractions like "1 2/3" or "1/2".
# We don't allow date like "1/2/34". No part of this is a fraction
fraction = (
    (Word(nums)('whole')
     + Word(nums)('numerator') + lit('/') + Word(nums)('denominator'))
    | Word(nums)('numerator') + lit('/') + Word(nums)('denominator')
)

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

shorthand_key = (
    kwd('ontag') | kwd('on tag')
    | kwd('specimens') | kwd('specimen')
    | kwd('catalog')
    | kwd('measurements length') | kwd('measurementslength')
    | kwd('measurements') | kwd('meas')
    | kwd('meas length') | kwd('measurementslength')
    | kwd('tag') + Word(nums)
    | kwd('mesurements') | kwd('measurementsnt')
)

sh_val = f' {number_re} | [?x]{{1,2}} '
sh_est = fr' \[? (?: {sh_val} ) \]? '
shorthand = Regex(fr"""
    (?<! [\d/-] )
    (?P<shorthand_tl> {sh_est} )
    (?P<shorthand_sep> [:/-] )
    (?P<shorthand_tal> {sh_est} )
    (?P=shorthand_sep)
    (?P<shorthand_hfl> {sh_est} )
    (?P=shorthand_sep)
    (?P<shorthand_el> {sh_est} )
    (?P<shorthand_ext> (?: (?P=shorthand_sep) [a-z]{{1,4}} {sh_est} )* )
    (?: [\s=:/-] \s*
        (?P<shorthand_wt_amb> \[? \s* )
        (?P<shorthand_wt> {sh_val} ) \s*
        \]?
        (?P<shorthand_wt_units> {metric_mass_re} )?
        \s*? \]?
    )?
    (?! [\d/:=-] )
    """, flags)
