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

fraction = LexRule('fraction', r"""
        (?<! [\d/,.] )
        (?: \d+ \s+ )? \d+ / \d+
        (?! [\d/,.] )
    """)

range = LexRule('range', r"""
        (?<! [\d/,.-]\d | \s+ to )
        (?&decimal) (?: \s* (?: - | to ) \s* (?&decimal) )?
        (?! [\d/,.-]\d | \s+ to )
        """)

cross = LexRule('cross', r"""
        (?<! [\d/,.-]\d | \s+ by )
        (?&decimal) (?: \s* (?: x | by | \* ) \s* (?&decimal) )?
        (?! [\d/,.-]\d | \s+ by )
    """)

shorthand_key = LexRule('shorthand_key', r"""
        on \s* tag | specimens? | catalog
        | meas (?: urements )? [:.,]{0,2} (?: \s* length \s* )?
            (?: \s* [({\[})]? [\p{Letter}]{1,2} [)}\]]? \.? )?
        | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
        | mesurements | Measurementsnt
    """)

shorthand = LexRule('shorthand', r"""
        (?<! [=:/-] )            # Handle list notation
        (?: (?&decimal) | [?x] )
        (?: [:-] (?: (?&decimal) | [?x]{1,2} ) ){3}
        (?: (?: [=:/-] | \s+ )
            (?: (?&decimal) | [?x] ) \s* (?&metric_wt)? )?
        (?! [=:/-] )          # Handle list notation
    """)

shorthand_mass = LexRule('shorthand_mass', r"""
        (?<! [:-] )            # Handle list notation
        (?: (?&decimal) | [?x] )
        (?: [:-] (?: (?&decimal) | [?x]{1,2} ) ){3}
        (?: (?: [=:-] | \s+ )
            (?: (?&decimal) | [?x] ) \s* (?&metric_wt)? )
        (?! [\s:/-] )          # Handle list notation
    """)

word = LexRule('word', util.boundary(r' \w+ '))   # Generic word

# Used to separate key1=value1; key2=val2 pairs
stop = LexRule('stop', r' [.;] ')

feet = LexRule('feet', r' (?: foot | feet | ft ) s? \.? ')

inches = LexRule('inches', r' (?: inch e? | in ) s? \.? ')

metric_len = LexRule('metric_len', r"""
        millimeters? | centimeters? | meters? | (?: [cm] [\s.]? m )
    """)

pounds = LexRule('pounds', r' (?: pound | lb ) s? \.? ')

ounces = LexRule('ounces', r' (?: ounce | oz ) s? \.? ')

metric_mass = LexRule('metric_mass', r""" (?&metric_wt) """)
