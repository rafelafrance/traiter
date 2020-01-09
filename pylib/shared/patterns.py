"""Shared token patterns."""

from pylib.stacked_regex.vocabulary import Vocabulary, FIRST, LAST
from pylib.vertnet.util import ordinal, number_to_words

VOCAB = Vocabulary()

# Chars that may be a token
VOCAB.part('slash', r' [/] ', capture=False)
VOCAB.part('dash', r' (?: – | - ) ', capture=False)
VOCAB.part('open', r' [(\[] ', capture=False)
VOCAB.part('close', r' [)\]] ', capture=False)
VOCAB.part('x', r' [x×] ', capture=False)
VOCAB.part('quest', r' [?] ')
VOCAB.part('comma', r' [,] ', capture=False, when=LAST)
VOCAB.part('semicolon', r' [;] ', capture=False, when=LAST)
VOCAB.part('ampersand', r' [&] ', capture=False)
VOCAB.part('eq', r' [=] ', capture=False)
VOCAB.part('under', r' [_] ', capture=False)
VOCAB.part('eol', r' [\n\r\l] ', capture=False)

# Small words
VOCAB.part('by', r' by ', capture=False)
VOCAB.part('to', r' to ', capture=False)
VOCAB.part('up_to', r' ( up \s+ )? to ', capture=False)
VOCAB.term('and', r' and ', capture=False)
VOCAB.term('conj', ' or and '.split(), capture=False)
VOCAB.term('prep', ' to with on of '.split(), capture=False)

# NOTE: Double quotes as inches is handled elsewhere
VOCAB.part('inches', r"""
    (?<! [a-z] ) ( inch e? s? | in s? (?! [a-ru-wyz] ) ) """)
VOCAB.part('feet', r"""
    (?<! [a-z] ) ( foot s? | feet s? | ft s? (?! [,\w]) ) | (?<= \d ) ' """)
VOCAB.part('metric_len', r"""
    ( milli | centi )? meters? | ( [cm] [\s.]? m ) (?! [a-ru-wyz] ) """)
VOCAB.grouper('len_units', ' metric_len feet inches'.split())

VOCAB.part('pounds', r' pounds? | lbs? ')
VOCAB.part('ounces', r' ounces? | ozs? ')
METRIC_MASS = r"""
    milligrams? | kilograms? | grams?
    | (?<! [a-z] )( m \.? g s? | k \.? \s? g a? | g[mr]? s? )(?! [a-z] )
    """
VOCAB.part('metric_mass', METRIC_MASS)
VOCAB.grouper('mass_units', 'metric_mass pounds ounces'.split())

VOCAB.grouper('us_units', 'feet inches pounds ounces'.split())
VOCAB.grouper('units', 'len_units mass_units'.split())

# # UUIDs cause problems when extracting certain shorthand notations.
VOCAB.part('uuid', r"""
    \b [0-9a-f]{8} - [0-9a-f]{4} - [1-5][0-9a-f]{3}
        - [89ab][0-9a-f]{3} - [0-9a-f]{12} \b """, capture=False, when=FIRST)

# Some numeric values are reported as ordinals or words
ORDINALS = [ordinal(x) for x in range(1, 6)]
VOCAB.part('ordinals', [number_to_words(x) for x in ORDINALS])

# Time units
VOCAB.part('time_units', r'years? | months? | weeks? | days? | hours?')

# Integers, no commas or signs and typically small
VOCAB.part('integer', r""" \d+ (?! [%\d\-] ) """)

# Date
VOCAB.part('month_name', """
    (?<! [a-z])
    (?P<month>
        january | february | march | april | may | june | july | august
        | september | october | november | december
        | jan | feb | mar | apr | jun | jul | aug | sept? | oct | nov | dec
    )
    (?! [a-z] )
    """, capture=False)
