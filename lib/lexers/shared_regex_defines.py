"""Regex defines used by more than one lexer."""

# pylint: disable=missing-docstring,invalid-name

from typing import List
from dataclasses import dataclass


@dataclass
class Define:
    label: str
    regex: str


Defines = List[Define]


# #############################################################################

def build_regex_defines(regex_defines: Defines):
    """Combine the ordered list of rules into one rule."""
    return '\n'.join(f'(?P<{d.label}> {d.regex} )' for d in regex_defines)


# #############################################################################

decimal = Define('decimal', r"""
        (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )?
    """)

metric_wt = Define('metric_wt', r"""
        (?: milligram | kilogram | gram ) s?
        | (?: m \.? g | k \.? g | g[mr]? ) s? \.?
    """)
