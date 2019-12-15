"""Shared token patterns."""

from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.util import ordinal, number_to_words

CATALOG = RuleCatalog()


# Chars that may be a token
CATALOG.part('slash', r' [/] ', capture=False)
CATALOG.part('dash', r' (?: – | - ) ', capture=False)
CATALOG.part('open', r' [(\[] ', capture=False)
CATALOG.part('close', r' [)\]] ', capture=False)
CATALOG.part('x', r' [x×] ', capture=False)
CATALOG.part('quest', r' [?] ')
CATALOG.part('comma', r' [,] ', capture=False)
CATALOG.part('semicolon', r' [;] ', capture=False)
CATALOG.part('ampersand', r' [&] ', capture=False)
CATALOG.part('eq', r' [=] ', capture=False)

# Small words
CATALOG.part('by', r' by ', capture=False)
CATALOG.part('to', r' to ', capture=False)
CATALOG.part('up_to', r' ( up \s+ )? to ', capture=False)
CATALOG.term('and', r' and ', capture=False)
CATALOG.term('conj', ' or and '.split(), capture=False)
CATALOG.term('prep', ' to with on of '.split(), capture=False)

# NOTE: Double quotes as inches is handled elsewhere
CATALOG.part('inches', r"""
    (?<! [a-z] ) ( inch e? s? | in s? (?! [a-ru-wyz] ) ) """)
CATALOG.part('feet', r"""
    (?<! [a-z] ) ( foot s? | feet s? | ft s? (?! [,\w]) ) | (?<= \d ) ' """)
CATALOG.part('metric_len', r"""
    ( milli | centi )? meters? | ( [cm] [\s.]? m ) (?! [a-ru-wyz] ) """)
CATALOG.grouper('len_units', ' metric_len feet inches'.split())

CATALOG.part('pounds', r' pounds? | lbs? ')
CATALOG.part('ounces', r' ounces? | ozs? ')
METRIC_MASS = r"""
    ( milligram | kilogram | gram ) ( s (?! [a-z]) )?
    | ( m \.? g | k \.? \s? g | g[mr]? ) ( s (?! [a-z]) )?
    """
CATALOG.part('metric_mass', METRIC_MASS)
CATALOG.grouper('mass_units', 'metric_mass pounds ounces'.split())

CATALOG.grouper('us_units', 'feet inches pounds ounces'.split())
CATALOG.grouper('units', 'len_units mass_units'.split())

# # UUIDs cause problems when extracting certain shorthand notations.
CATALOG.part('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """, capture=False)

# Some numeric values are reported as ordinals or words
ORDINALS = [ordinal(x) for x in range(1, 6)]
CATALOG.part('ordinals', [number_to_words(x) for x in ORDINALS])

# Time units
CATALOG.part('time_units', r'years? | months? | weeks? | days? | hours?')

# integers, no commas or signs and typically small
CATALOG.part('integer', r""" \d+ (?! [%\d\-] ) """)
