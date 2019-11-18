"""Shared token patterns."""

from pylib.stacked_regex.rule import fragment, keyword, replacer, InRegexp
from pylib.vertnet.util import ordinal, number_to_words


SCANNER = {}
REPLACER = {}


def add_frag(name: str, regexp: InRegexp) -> None:
    """Add a rule to SCANNER."""
    SCANNER[name] = fragment(name, regexp)


def add_key(name: str, regexp: InRegexp) -> None:
    """Add a rule to SCANNER."""
    SCANNER[name] = keyword(name, regexp)


def add_repl(name: str, regexp: InRegexp) -> None:
    """Add a rule to SCANNER."""
    REPLACER[name] = replacer(name, regexp)


# Chars that may be a token
add_frag('slash', r' [/] ')
add_frag('dash', r' (?: – | - ) ')
add_frag('open', r' [(\[] ')
add_frag('close', r' [)\]] ')
add_frag('x', r' [x×] ')
add_frag('quest', r' [?] ')

# Small words
add_frag('by', r' by ')
add_frag('to', r' to ')

# NOTE: Double quotes as inches is handled elsewhere
add_frag('inches', ' ( inch e? s? | in s? ) \b ')

add_frag('feet', r" foot s? | feet s? | ft s? (?! [,\w]) | (?<= \d ) ' ")
add_frag('metric_len', r' ( milli | centi )? meters? | ( [cm] [\s.]? m ) ')

add_frag(
    'len_units', '|'.join(
        [SCANNER[x].pattern for x in ('metric_len', 'feet', 'inches')]))

add_frag('pounds', r' pounds? | lbs? ')
add_frag('ounces', r' ounces? | ozs? ')
add_frag('metric_mass', r"""
    ( milligram | kilogram | gram ) ( s (?! [a-z]) )?
    | ( m \.? g | k \.? \s? g | g[mr]? )
        ( s (?! [a-z]) )?
    """)

add_frag('us_mass', '|'.join([
    SCANNER[x].pattern for x in ('pounds', 'ounces')]))

add_frag('mass_units', '|'.join([
    SCANNER[x].pattern for x in ('metric_mass', 'pounds', 'ounces')]))

# Numbers are positive decimals
add_frag('number', r"""
    ( \d{1,3} ( , \d{3} ){1,3} | \d+ ) ( \. \d+ )?
    | (?<= [^\d] ) \. \d+ | ^ \. \d+
    """)

# A number or a range of numbers like "12 to 34" or "12.3-45.6"
# Note we want to exclude dates and to not pick up partial dates
# So: no part of "2014-12-11" would be in a range
add_repl('range', """  (?<! dash ) number ( dash | to ) number (?! dash ) """)

# A number times another number like: "12 x 34" this is typically
# length x width. We Allow a triple like "12 x 34 x 56" but we ony take
# the first two numbers
add_repl('cross', """ (?<! x ) number ( x | by ) number """)

# For fractions like "1 2/3" or "1/2".
# We don't allow dates like "1/2/34".
add_repl('fraction', """ (?<! slash ) number slash number (?! slash ) """)

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
