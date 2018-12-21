"""Rules used by more than one lexer."""

# pylint: disable=missing-docstring,invalid-name,redefined-builtin

from typing import List
from dataclasses import dataclass
import lib.lexers.shared_utils as util


@dataclass
class LexRule:
    token: str
    regex: str


LexRules = List[LexRule]


# #############################################################################

def build_lex_rules(lex_rules: LexRules):
    """Combine the ordered list of rules into one rule."""
    return '\n| '.join([f' (?P<{r.token}> {r.regex} ) ' for r in lex_rules])


# #############################################################################

# Numbers are positive decimals
number = LexRule('number', ' (?&decimal) ')

# For fractions like "1 2/3" or "1/2".
# We don't allow date like "1/2/34". No part of this is a fraction
fraction = LexRule('fraction', r"""
    (?<! [\d/,.] )
    (?: \d+ \s+ )? \d+ / \d+
    (?! [\d/,.] )
    """)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
range = LexRule('range', r"""
    (?<! \d+ | \d [/,.-] | to \s+ )
    (?&decimal) (?: \s* (?&range_sep) \s* (?&decimal) )?
    (?! [/,.-] \d | \d+ | \s+ to )
    """)

# A number times another number like "12 x 34" this is typically length x width
# We Allow a triple like "12 x 34 x 56" but we ony take the first two numbers
cross = LexRule('cross', r"""
    (?<! [\d/,.-]\d | \s+ by )
    (?&decimal) (?: \s* (?: x | by | \* ) \s* (?&decimal) )?
    # (?! [\d/,.-]\d | \s+ by )
    """)

shorthand_key = LexRule('shorthand_key', r"""
    on \s* tag | specimens? | catalog
    | meas (?: urements )? [:.,]{0,2} (?: \s* length \s* )?
        (?: \s* [({\[})]? [\p{Letter}]{1,2} [)}\]]? \.? )?
    | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
    | mesurements | Measurementsnt
    """)

# This is a common notation form. "11-22-33-44:55g". There are other separators
#   11 = total length (ToL or TL)
#   22 = tail length (TaL)
#   33 = hind foot length (HFL)
#   44 = ear length (EL)
#   55 = body mass is optional, as is the mass units
# Unknown values are filled with ? or x. Like 11-xx-xx-44 or 11-??-33-44
shorthand = LexRule('shorthand', r"""
    (?<! (?&shorthand_overrun) )
    (?&shorthand_vals) (?&shorthand_wt)?
    (?! (?&shorthand_overrun) )
    """)

# This is like "shorthand" above with the difference being that we are forcing
# the mass to be present. This is, unsurprisingly, used when parsing body mass.
shorthand_mass = LexRule('shorthand_mass', r"""
    (?<! (?&shorthand_overrun) )
    (?&shorthand_vals) (?&shorthand_wt)
    (?! (?&shorthand_overrun) )
    """)

# Generic word
word = LexRule('word', util.boundary(r' \w+ '))

# Used to separate key1=value1; key2=val2 pairs
sep = LexRule('sep', r' [.;] ')

feet = LexRule('feet', r' (?: foot | feet | ft ) s? \.? ')

inches = LexRule('inches', r' (?: inch e? | in ) s? \.? ')

metric_len = LexRule('metric_len', r"""
        millimeters? | centimeters? | meters? | (?: [cm] [\s.]? m )
    """)

pounds = LexRule('pounds', r' (?: pound | lb ) s? \.? ')

ounces = LexRule('ounces', r' (?: ounce | oz ) s? \.? ')

metric_mass = LexRule('metric_mass', r""" (?&metric_wt) """)
