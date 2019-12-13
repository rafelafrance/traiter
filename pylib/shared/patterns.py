"""Shared token patterns."""

from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.util import ordinal, number_to_words

CAT = RuleCatalog()
RULE = CAT.rules


# Chars that may be a token
CAT.part('slash', r' [/] ', capture=False)
CAT.part('dash', r' (?: – | - ) ', capture=False)
CAT.part('open', r' [(\[] ', capture=False)
CAT.part('close', r' [)\]] ', capture=False)
CAT.part('x', r' [x×] ', capture=False)
CAT.part('quest', r' [?] ')
CAT.part('comma', r' [,] ', capture=False)
CAT.part('semicolon', r' [;] ', capture=False)
CAT.part('ampersand', r' [&] ', capture=False)
CAT.part('eq', r' [=] ', capture=False)

# Small words
CAT.part('by', r' by ', capture=False)
CAT.part('to', r' to ', capture=False)
CAT.part('up_to', r' ( up \s+ )? to ', capture=False)
CAT.term('and', r' and ', capture=False)
CAT.term('conj', ' or and '.split(), capture=False)
CAT.term('prep', ' to with on of '.split(), capture=False)

# NOTE: Double quotes as inches is handled elsewhere
CAT.part('inches', r"""
    (?<! [a-z] ) ( inch e? s? | in s? (?! [a-ru-wyz] ) ) """)
CAT.part('feet', r"""
    (?<! [a-z] ) ( foot s? | feet s? | ft s? (?! [,\w]) ) | (?<= \d ) ' """)
CAT.part('metric_len', r"""
    ( milli | centi )? meters? | ( [cm] [\s.]? m ) (?! [a-ru-wyz] ) """)
CAT.grouper('len_units', ' metric_len feet inches'.split())

CAT.part('pounds', r' pounds? | lbs? ')
CAT.part('ounces', r' ounces? | ozs? ')
CAT.part('metric_mass', r"""
    ( milligram | kilogram | gram ) ( s (?! [a-z]) )?
    | ( m \.? g | k \.? \s? g | g[mr]? ) ( s (?! [a-z]) )?
    """)
CAT.grouper('mass_units', 'metric_mass pounds ounces'.split())

CAT.grouper('us_units', 'feet inches pounds ounces'.split())
CAT.grouper('units', 'len_units mass_units'.split())

# # UUIDs cause problems when extracting certain shorthand notations.
CAT.part('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """, capture=False)

# Some numeric values are reported as ordinals or words
ORDINALS = [ordinal(x) for x in range(1, 6)]
CAT.part('ordinals', [number_to_words(x) for x in ORDINALS])

# Time units
CAT.part('time_units', r'years? | months? | weeks? | days? | hours?')

# integers, no commas or signs and typically small
CAT.part('integer', r""" \d+ (?! [%\d\-] ) """)
