"""Regexp defines used by more than one lexer."""

from typing import List
from dataclasses import dataclass
import regex


@dataclass
class Regexp:
    """Label a regex so it can be reused."""

    label: str
    regex: str


Regexps = List[Regexp]


# #############################################################################

def boundary(regex, left=True, right=True):
    r"""Wrap a regular expression in \b character class.

    This is used to "delimit" a word on a word boundary so the regex does
    not match the interior of a word.

    - This is helpful for keyword searches like 't'. Without this 't' would
      match both 't's in 'that' but the regex in \b neither 't' is matched.
      Only 't's like ' t ', or '$t.', etc. will match.
    - It is not helpful for searching for things like '19mm' where there is
      no word break between the two tokens.
    - It is also not helpful if your pattern ends or starts with a non-word
      character.
    """
    left = r'\b' if left else ''
    right = r'\b' if right else ''
    return r'{} (?: {} ) {}'.format(left, regex, right)


def build_lex_rules(lex_rules: Regexps):
    """Combine the ordered list of rules into one rule."""
    return '\n| '.join([f' (?P<{r.label}> {r.regex} ) ' for r in lex_rules])


def build_regex_defines(regexes: Regexps):
    """Combine the ordered list of rules into one rule."""
    defines = '\n'.join(f'(?P<{d.label}> {d.regex} )' for d in regexes)
    return f'(?(DEFINE) {defines} )'


def compile_regex(label):
    """Compile one define as a plain regex."""
    regexp = [regex.compile(d.regex, regex.VERBOSE | regex.IGNORECASE)
              for d in ALL if d.label == label]
    return regexp[0]


# #############################################################################

ALL = [
    Regexp('decimal', r"""
        (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )?
        """),

    Regexp('metric_wt', r"""
        (?: milligram | kilogram | gram ) s?
        | (?: m \.? g | k \.? g | g[mr]? ) s? \.?
        """),

    Regexp('range_sep', r""" - | to """),

    Regexp('shorthand_overrun', r""" [\d/-] """),

    Regexp('shorthand_val', r"""
        (?: (?&decimal) | [?x]{1,2} )
        """),

    Regexp('shorthand_sep', r""" [:-] """),

    Regexp('shorthand_vals', r"""
        (?&shorthand_val)
        (?: (?&shorthand_sep) (?&shorthand_val) ){3}
        """),

    Regexp('shorthand_wt_sep', r"""
        [\s=:/-]
        """),

    Regexp('shorthand_wt', r"""
        (?&shorthand_wt_sep) \s* (?&shorthand_val) \s* (?&metric_wt)?
        """),
]

# #############################################################################

# Numbers are positive decimals
number = Regexp('number', ' (?&decimal) ')

# For fractions like "1 2/3" or "1/2".
# We don't allow date like "1/2/34". No part of this is a fraction
fraction = Regexp('fraction', r"""
    (?<! [\d/,.] )
    (?: \d+ \s+ )? \d+ / \d+
    (?! [\d/,.] )
    """)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
range = Regexp('range', r"""
    (?<! \d+ | \d [/,.-] | to \s+ )
    (?&decimal) (?: \s* (?&range_sep) \s* (?&decimal) )?
    (?! [/,.-] \d | \d+ | \s+ to )
    """)

# A number times another number like "12 x 34" this is typically length x width
# We Allow a triple like "12 x 34 x 56" but we ony take the first two numbers
cross = Regexp('cross', r"""
    (?<! [\d/,.-]\d | \s+ by )
    (?&decimal) (?: \s* (?: x | by | \* ) \s* (?&decimal) )?
    # (?! [\d/,.-]\d | \s+ by )
    """)

shorthand_key = Regexp('shorthand_key', r"""
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
shorthand = Regexp('shorthand', r"""
    (?<! (?&shorthand_overrun) )
    (?&shorthand_vals) (?&shorthand_wt)?
    (?! (?&shorthand_overrun) )
    """)

# This is like "shorthand" above with the difference being that we are forcing
# the mass to be present. This is, unsurprisingly, used when parsing body mass.
shorthand_mass = Regexp('shorthand_mass', r"""
    (?<! (?&shorthand_overrun) )
    (?&shorthand_vals) (?&shorthand_wt)
    (?! (?&shorthand_overrun) )
    """)

# Generic word
word = Regexp('word', boundary(r' \w+ '))

# Used to separate key1=value1; key2=val2 pairs
sep = Regexp('sep', r' [.;] ')

feet = Regexp('feet', r' (?: foot | feet | ft ) s? \.? ')

inches = Regexp('inches', r' (?: inch e? | in ) s? \.? ')

metric_len = Regexp('metric_len', r"""
        millimeters? | centimeters? | meters? | (?: [cm] [\s.]? m )
    """)

pounds = Regexp('pounds', r' (?: pound | lb ) s? \.? ')

ounces = Regexp('ounces', r' (?: ounce | oz ) s? \.? ')

metric_mass = Regexp('metric_mass', r""" (?&metric_wt) """)
