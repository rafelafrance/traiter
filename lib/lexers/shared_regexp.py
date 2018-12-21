"""Regexp defines used by more than one lexer."""

from typing import List
from dataclasses import dataclass
import regex


@dataclass
class Regexp:
    """Label a regexp so it can be reused."""

    label: str
    regexp: str


Regexps = List[Regexp]


# #############################################################################

def boundary(regexp, left=True, right=True):
    r"""Wrap a regular expression in \b character class.

    This is used to "delimit" a word on a word boundary so the regexp does
    not match the interior of a word.

    - This is helpful for keyword searches like 't'. Without this 't' would
      match both 't's in 'that' but the regexp in \b neither 't' is matched.
      Only 't's like ' t ', or '$t.', etc. will match.
    - It is not helpful for searching for things like '19mm' where there is
      no word break between the two tokens.
    - It is also not helpful if your pattern ends or starts with a non-word
      character.
    """
    left = r'\b' if left else ''
    right = r'\b' if right else ''
    return r'{} (?: {} ) {}'.format(left, regexp, right)


def build_lex_rules(lex_rules: Regexps):
    """Combine the ordered list of rules into one rule."""
    return '\n| '.join([f' (?P<{r.label}> {r.regexp} ) ' for r in lex_rules])


def build_regex_defines(regexes: Regexps):
    """Combine the ordered list of rules into one rule."""
    defines = '\n'.join(f'(?P<{d.label}> {d.regexp} )' for d in regexes)
    return f'(?(DEFINE) {defines} )'


def get(label):
    """Get the regular expression associated with the given label."""
    regexp = [r for r in ALL if r.label == label]
    if not regexp:
        raise ValueError(f'Could not find the regexp {label}')
    return regexp[0]


def compile_regex(label):
    """Compile one define as a plain regex."""
    regexp = get(label)
    return regex.compile(regexp.regexp, regex.VERBOSE | regex.IGNORECASE)


# #############################################################################
# These regexp are typically used as (?(DEFINE) <label> ... ) clauses

DEFINES = [
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

    Regexp('shorthand_ext', r"""
        (?: (?&shorthand_sep) [\p{Letter}]{1,4} (?&shorthand_val) )
        """),

    Regexp('shorthand_wt', r"""
        (?&shorthand_wt_sep) \s* (?&shorthand_val) \s* (?&metric_wt)?
        """),
]

# #############################################################################
# These regexp are typically used as lexer rules.

LEX_RULES = [
    # Numbers are positive decimals
    Regexp('number', ' (?&decimal) '),


    # For fractions like "1 2/3" or "1/2".
    # We don't allow date like "1/2/34". No part of this is a fraction
    Regexp('fraction', r"""
        (?<! [\d/,.] )
        (?: \d+ \s+ )? \d+ / \d+
        (?! [\d/,.] )
        """),

    # A number or a range of numbers like "12 to 34" or "12.3-45.6"
    # Note we want to exclude dates and to not pick up partial dates
    # So: no part of "2014-12-11" would be in a range
    Regexp('range', r"""
        (?<! \d+ | \d [/,.-] | to \s+ )
        (?&decimal) (?: \s* (?&range_sep) \s* (?&decimal) )?
        (?! [/,.-] \d | \d+ | \s+ to )
        """),

    # A number times another number like "12 x 34" this is typically
    # length x width. We Allow a triple like "12 x 34 x 56" but we ony take the
    # first two numbers
    Regexp('cross', r"""
        (?<! [\d/,.-]\d | \s+ by )
        (?&decimal) (?: \s* (?: x | by | \* ) \s* (?&decimal) )?
        # (?! [\d/,.-]\d | \s+ by )
        """),

    Regexp('shorthand_key', r"""
        on \s* tag | specimens? | catalog
        | meas (?: urements )? [:.,]{0,2} (?: \s* length \s* )?
            (?: \s* [({\[})]? [\p{Letter}]{1,2} [)}\]]? \.? )?
        | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
        | mesurements | Measurementsnt
        """),

    # This is a common notation form: "11-22-33-44:99g".
    # There are other separators.
    # There is also an extended form that looks like:
    #   ""11-22-33-44-fa55-hb66:99g"" There may be several extended numbers.
    #
    #   11 = total length (ToL or TL)
    #   22 = tail length (TaL)
    #   33 = hind foot length (HFL)
    #   44 = ear length (EL)
    #   99 = body mass is optional, as is the mass units
    # Unknown values are filled with ? or x. Like 11-xx-xx-44 or 11-??-33-44
    Regexp('shorthand', r"""
        (?<! (?&shorthand_overrun) )
        (?&shorthand_vals)
        (?&shorthand_ext)*
        (?&shorthand_wt)?
        (?! (?&shorthand_overrun) )
        """),

    # This is like "shorthand" above with the difference being that we are
    # forcing the mass to be present. This is, unsurprisingly, used when
    # parsing body mass.
    Regexp('shorthand_mass', r"""
        (?<! (?&shorthand_overrun) )
        (?&shorthand_vals)
        (?&shorthand_ext)*
        (?&shorthand_wt)
        (?! (?&shorthand_overrun) )
        """),

    # Generic word
    Regexp('word', boundary(r' \w+ ')),

    # Used to separate key1=value1; key2=val2 pairs
    Regexp('sep', r' [.;] '),

    Regexp('feet', r' (?: foot | feet | ft ) s? \.? '),

    Regexp('inches', r' (?: inch e? | in ) s? \.? '),

    Regexp('metric_len', r"""
            millimeters? | centimeters? | meters? | (?: [cm] [\s.]? m )
        """),

    Regexp('pounds', r' (?: pound | lb ) s? \.? '),

    Regexp('ounces', r' (?: ounce | oz ) s? \.? '),

    Regexp('metric_mass', r""" (?&metric_wt) """),

]


# #############################################################################

ALL = DEFINES + LEX_RULES
