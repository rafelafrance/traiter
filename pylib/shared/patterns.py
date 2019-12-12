"""Shared token patterns."""

from pylib.shared.rule_set import RuleSet
from pylib.vertnet.util import ordinal, number_to_words

SET = RuleSet()
RULE = SET.rules


# Chars that may be a token
SET.add_frag('slash', r' [/] ', capture=False)
SET.add_frag('dash', r' (?: – | - ) ', capture=False)
SET.add_frag('open', r' [(\[] ', capture=False)
SET.add_frag('close', r' [)\]] ', capture=False)
SET.add_frag('x', r' [x×] ', capture=False)
SET.add_frag('quest', r' [?] ')
SET.add_frag('comma', r' [,] ', capture=False)
SET.add_frag('semicolon', r' [;] ', capture=False)
SET.add_frag('ampersand', r' [&] ', capture=False)
SET.add_frag('eq', r' [=] ', capture=False)

# Small words
SET.add_frag('by', r' by ', capture=False)
SET.add_frag('to', r' to ', capture=False)
SET.add_frag('up_to', r' ( up \s+ )? to ', capture=False)
SET.add_key('and', r' and ', capture=False)
SET.add_key('conj', ' or and '.split(), capture=False)
SET.add_key('prep', ' to with on of '.split(), capture=False)

# NOTE: Double quotes as inches is handled elsewhere
SET.add_frag('inches', r"""
    (?<! [a-z] ) ( inch e? s? | in s? (?! [a-ru-z] ) ) """)
SET.add_frag('feet', r"""
    (?<! [a-z] ) ( foot s? | feet s? | ft s? (?! [,\w]) ) | (?<= \d ) ' """)
SET.add_frag('metric_len', r"""
    ( milli | centi )? meters? | ( [cm] [\s.]? m ) (?! [a-ru-z] ) """)
SET.add_group('len_units', ' metric_len feet inches'.split())

SET.add_frag('pounds', r' pounds? | lbs? ')
SET.add_frag('ounces', r' ounces? | ozs? ')
SET.add_frag('metric_mass', r"""
    ( milligram | kilogram | gram ) ( s (?! [a-z]) )?
    | ( m \.? g | k \.? \s? g | g[mr]? ) ( s (?! [a-z]) )?
    """)
SET.add_group('mass_units', 'metric_mass pounds ounces'.split())

SET.add_group('us_units', 'feet inches pounds ounces'.split())
SET.add_group('units', 'len_units mass_units'.split())

# # UUIDs cause problems when extracting certain shorthand notations.
SET.add_frag('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """, capture=False)

# Some numeric values are reported as ordinals or words
ORDINALS = [ordinal(x) for x in range(1, 6)]
SET.add_frag('ordinals', [number_to_words(x) for x in ORDINALS])

# Time units
SET.add_frag('time_units', r'years? | months? | weeks? | days? | hours?')

# integers, no commas or signs and typically small
SET.add_frag('integer', r""" \d+ (?! [%\d\-] ) """)
