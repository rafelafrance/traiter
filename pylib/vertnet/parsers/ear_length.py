"""Parse ear length notations."""

from functools import partial
import regex
from pylib.shared.util import FLAGS
from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.numeric import simple_len, fraction, shorthand_length
from pylib.vertnet.numeric import numeric_fix_ups
import pylib.vertnet.shared_patterns as patterns

CATALOG = RuleCatalog(patterns.CATALOG)

# How far to look into the surrounding context to disambiguate the parse
LOOK_BACK_FAR = 40
LOOK_BACK_NEAR = 10

# These indicate that the parse is not really for an ear length
IS_ET = regex.compile(r' e \.? t ', FLAGS)
IS_NUMBER = regex.compile(' [#] ', FLAGS)
IS_MAG = regex.compile(' magnemite ', FLAGS)
IS_ID = regex.compile(' identifier | ident | id ', FLAGS)

# The 'E' abbreviation gets confused with abbreviation for East sometimes.
# Try to disambiguate the two by looking for a North near by.
LOOK_AROUND = 10
IS_EAST = regex.compile(r' \b n ', FLAGS)


def fix_up(trait, text):
    """Fix problematic parses."""
    # Problem parses happen mostly with an ambiguous key
    if trait.ambiguous_key:

        # "E.T." is not an ear length measurement
        start = max(0, trait.start - LOOK_BACK_NEAR)
        if (IS_ET.search(text, start, trait.start)
                or IS_NUMBER.search(text, start, trait.start)):
            return None

        # Magnemite confounds the abbreviation
        start = max(0, trait.start - LOOK_BACK_FAR)
        if (IS_MAG.search(text, start, trait.start)
                or IS_ID.search(text, start, trait.start)):
            return None

        # Make sure it's not actually an abbreviation for "East"
        start = max(0, trait.start - LOOK_AROUND)
        end = min(len(text), trait.end + LOOK_AROUND)
        if (IS_EAST.search(text, start, trait.start)
                or IS_EAST.search(text, trait.end, end)):
            return None

    # Try to disambiguate doubles quotes from inches
    return numeric_fix_ups(trait, text)


EAR_LENGTH = Base(
    name=__name__.split('.')[-1],
    fix_up=fix_up,
    rules=[

        CATALOG['uuid'],  # UUIDs cause problems with numbers

        # Units are in the key, like: EarLengthInMillimeters
        CATALOG.term('key_with_units', r"""
            ear \s* ( length | len ) \s* in \s*
            (?P<len_units> millimeters | mm )
            """),

        # Abbreviation containing the measured from notation, like: e/n or e/c
        CATALOG.part('char_measured_from', r"""
            (?<! [a-z] ) (?<! [a-z] \s )
            (?P<ambiguous_key> e ) /? (?P<measured_from1> n | c ) [-]?
            (?! \.? [a-z] )
            """),

        # The abbreviation key, just: e. This can be a problem.
        CATALOG.part('char_key', r"""
            (?<! \w ) (?<! \w \s )
            (?P<ambiguous_key> e )
            (?! \.? \s? [a-z\(] )
            """),

        # Standard keywords that indicate an ear length follows
        CATALOG.term('keyword', [
            r' ear \s* from \s* (?P<measured_from1> notch | crown )',
            r' ear \s* ( length | len )',
            r' ear (?! \s* tag )',
            r' ef (?P<measured_from2> n | c ) [-]?',
        ]),

        # Some patterns require a separator
        CATALOG['word'],
        CATALOG.part('sep', r' [;,] '),

        # Consider any of the following as just a key
        CATALOG.grouper('key', 'keyword char_key char_measured_from'.split()),

        # Handle fractional values like: ear 9/16"
        CATALOG.producer(fraction, 'key fraction (?P<units> len_units )?'),

        # E.g.: earLengthInMM 9-10
        CATALOG.producer(simple_len, '(?P<key> key_with_units ) len_range'),

        # E.g.: ear 9-10 mm
        CATALOG.producer(simple_len, 'key len_range (?P<units> len_units )?'),

        # Shorthand notation like: on tag: 11-22-33-44=99g
        CATALOG.producer(
            partial(shorthand_length, measurement='shorthand_el'), [
                'shorthand_key shorthand',  # With a key
                'shorthand',  # Without a key
            ]),
    ],
)
