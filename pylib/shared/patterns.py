"""Shared token patterns."""

from pylib.stacked_regex.rule import Rules, fragment, keyword, grouper
from pylib.stacked_regex.rule import InRegexp
from pylib.vertnet.util import ordinal, number_to_words

RULE = {}


def add_frag(name: str, regexp: InRegexp, capture=True) -> None:
    """Add a rule to RULE."""
    RULE[name] = fragment(name, regexp, capture=capture)


def add_key(name: str, regexp: InRegexp, capture=True) -> None:
    """Add a rule to RULE."""
    RULE[name] = keyword(name, regexp, capture=capture)


def add_group(name: str, regexp: InRegexp, capture=True) -> None:
    """Add a rule to RULE."""
    RULE[name] = grouper(name, regexp, capture=capture)


def add_set(name: str, rules: Rules) -> None:
    """Add a rule set."""
    RULE[name] = rules


# Chars that may be a token
add_frag('slash', r' [/] ', capture=False)
add_frag('dash', r' (?: – | - ) ', capture=False)
add_frag('open', r' [(\[] ', capture=False)
add_frag('close', r' [)\]] ', capture=False)
add_frag('x', r' [x×] ', capture=False)
add_frag('quest', r' [?] ')
add_frag('comma', r' [,] ', capture=False)
add_frag('semicolon', r' [;] ', capture=False)
add_frag('ampersand', r' [&] ', capture=False)

# Small words
add_frag('by', r' by ', capture=False)
add_frag('to', r' to ', capture=False)
add_frag('up_to', r' ( up \s+ )? to ', capture=False)
add_key('and', r' and ', capture=False)
add_key('conj', ' or and '.split(), capture=False)
add_key('prep', ' to with on of '.split(), capture=False)

# NOTE: Double quotes as inches is handled elsewhere
add_frag('inches', r' ( inch e? s? | \b in s? ) \b ')
add_frag('feet', r" foot s? | feet s? | ft s? (?! [,\w]) | (?<= \d ) ' ")
add_frag('metric_len', r' ( milli | centi )? meters? | ( [cm] [\s.]? m ) ')
add_group('len_units', ' metric_len feet inches'.split())

add_frag('pounds', r' pounds? | lbs? ')
add_frag('ounces', r' ounces? | ozs? ')
add_frag('metric_mass', r"""
    ( milligram | kilogram | gram ) ( s (?! [a-z]) )?
    | ( m \.? g | k \.? \s? g | g[mr]? ) ( s (?! [a-z]) )?
    """)
add_group('mass_units', 'metric_mass pounds ounces'.split())

add_group('us_units', 'feet inches pounds ounces'.split())
add_group('units', 'len_units mass_units'.split())


# # UUIDs cause problems when extracting certain shorthand notations.
add_frag('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """, capture=False)

# Some numeric values are reported as ordinals or words
ORDINALS = [ordinal(x) for x in range(1, 6)]
add_frag('ordinals', [number_to_words(x) for x in ORDINALS])

# Time units
add_frag('time_units', r'years? | months? | weeks? | days? | hours?')

# integers, no commas or signs and typically small
add_frag('integer', r""" \d+ (?! [%\d\-] ) """)
