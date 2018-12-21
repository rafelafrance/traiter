"""Regex defines used by more than one lexer."""

# pylint: disable=missing-docstring

from typing import List
from dataclasses import dataclass
import regex


@dataclass
class Regex:
    label: str
    regex: str


Regexes = List[Regex]


# #############################################################################

def build_regex_defines(regexes: Regexes):
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
    Regex('decimal', r"""
        (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )?
        """),

    Regex('metric_wt', r"""
        (?: milligram | kilogram | gram ) s?
        | (?: m \.? g | k \.? g | g[mr]? ) s? \.?
        """),

    Regex('range_sep', r""" - | to """),

    Regex('shorthand_overrun', r""" [\d/-] """),

    Regex('shorthand_val', r"""
        (?: (?&decimal) | [?x]{1,2} )
        """),

    Regex('shorthand_sep', r""" [:-] """),

    Regex('shorthand_vals', r"""
        (?&shorthand_val)
        (?: (?&shorthand_sep) (?&shorthand_val) ){3}
        """),

    Regex('shorthand_wt_sep', r"""
        [\s=:/-]
        """),

    Regex('shorthand_wt', r"""
        (?&shorthand_wt_sep) \s* (?&shorthand_val) \s* (?&metric_wt)?
        """),
]
