"""Shared token patterns."""

from pylib.stacked_regex.rule import Rules, fragment, keyword, replacer
from pylib.stacked_regex.rule import InRegexp
from pylib.vertnet.util import ordinal, number_to_words

RULE = {}


def add_frag(name: str, regexp: InRegexp) -> None:
    """Add a rule to RULE."""
    RULE[name] = fragment(name, regexp)


def add_key(name: str, regexp: InRegexp) -> None:
    """Add a rule to RULE."""
    RULE[name] = keyword(name, regexp)


def add_rep(name: str, regexp: InRegexp) -> None:
    """Add a rule to RULE."""
    RULE[name] = replacer(name, regexp)


def add_set(name: str, rules: Rules) -> None:
    """Add a rule set."""
    RULE[name] = rules


# Chars that may be a token
add_frag('slash', r' [/] ')
add_frag('dash', r' (?: – | - ) ')
add_frag('open', r' [(\[] ')
add_frag('close', r' [)\]] ')
add_frag('x', r' [x×] ')
add_frag('quest', r' [?] ')
add_frag('comma', r' [,] ')

# Small words
add_frag('by', r' by ')
add_frag('to', r' to ')

# NOTE: Double quotes as inches is handled elsewhere
add_frag('inches', ' ( inch e? s? | in s? ) \b ')
add_frag('feet', r" foot s? | feet s? | ft s? (?! [,\w]) | (?<= \d ) ' ")
add_frag('metric_len', r' ( milli | centi )? meters? | ( [cm] [\s.]? m ) ')
add_rep('len_units', ' metric_len feet inches'.split())

add_frag('pounds', r' pounds? | lbs? ')
add_frag('ounces', r' ounces? | ozs? ')
add_frag('metric_mass', r"""
    ( milligram | kilogram | gram ) ( s (?! [a-z]) )?
    | ( m \.? g | k \.? \s? g | g[mr]? ) ( s (?! [a-z]) )?
    """)
add_rep('mass_units', 'metric_mass pounds ounces'.split())

add_rep('us_units', 'feet inches pounds ounces'.split())
add_rep('units', 'len_units mass_units'.split())

# Numbers are positive decimals
add_frag('number', r"""
    (?P<estimated_value> \[ )? 
    ( ( \d{1,3} ( , \d{3} ){1,3} | \d+ ) ( \. \d+ )?
        | (?<= [^\d] ) \. \d+ | ^ \. \d+ )
    \]?
    """)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
add_rep('range', """
    (?<! dash ) 
    ( number units? (( dash | to ) number units?)? ) 
    (?! dash ) """)
# Rule set for parsing a range
add_set('range_set', [
    RULE['inches'],
    RULE['feet'],
    RULE['metric_len'],
    RULE['len_units'],
    RULE['pounds'],
    RULE['ounces'],
    RULE['metric_mass'],
    RULE['mass_units'],
    RULE['units'],
    RULE['number'],
    RULE['dash'],
    RULE['to'],
    RULE['range'],
])

# A rule for parsing a compound weight like 2 lbs. 3.1 - 4.5 oz
add_rep('compound_wt', """
    (?P<lbs> number ) pounds comma?
    (?P<ozs> number ) ( ( dash | to ) (?P<ozs> number ) )? ounces
    """)
# Rule set for parsing a compound_wt
add_set('compound_wt_set', [
    RULE['pounds'],
    RULE['ounces'],
    RULE['number'],
    RULE['dash'],
    RULE['comma'],
    RULE['to'],
    RULE['compound_wt'],
])

# A number times another number like: "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we ony take
# the first two numbers
add_rep('cross', """
    (?<! x ) 
        ( number len_units? ( x | by ) number len_units? 
        | number len_units ) """)
# Rule set for parsing a cross
add_set('cross_set', [
    RULE['inches'],
    RULE['feet'],
    RULE['metric_len'],
    RULE['len_units'],
    RULE['number'],
    RULE['x'],
    RULE['by'],
    RULE['cross'],
])

# For fractions like "1 2/3" or "1/2".
# We don't allow dates like "1/2/34".
add_rep('fraction', """ (?<! slash ) number slash number (?! slash ) units? """)
# Rule set for parsing fractions
add_set('fraction_set', [
    RULE['inches'],
    RULE['feet'],
    RULE['metric_len'],
    RULE['len_units'],
    RULE['pounds'],
    RULE['ounces'],
    RULE['metric_mass'],
    RULE['mass_units'],
    RULE['units'],
    RULE['number'],
    RULE['slash'],
    RULE['fraction'],
])

# # UUIDs cause problems when extracting certain shorthand notations.
add_frag('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """)

# Some numeric values are reported as ordinals or words
ORDINALS = [ordinal(x) for x in range(1, 6)]
ORDINALS += [number_to_words(x) for x in ORDINALS]
add_frag('ordinals', ' | '.join(ORDINALS))

# Some numeric values are reported as ordinals or words
ORDINALS = [ordinal(x) for x in range(1, 6)]
ORDINALS += [number_to_words(x) for x in ORDINALS]
add_frag('ordinals', ' | '.join(ORDINALS))

# Time units
add_frag('time_units', r'years? | months? | weeks? | days? | hours?')

# integers, no commas or signs and typically small
add_frag('integer', r""" \d+ (?! [%\d\-] ) """)
