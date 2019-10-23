"""Parse ear length notations."""

import re
from functools import partial
from stacked_regex.rule import fragment, keyword, producer, replacer
from pylib.parsers.base import Base
from pylib.parsers.numeric import simple, fraction, shorthand_length
from pylib.parsers.numeric import numeric_fix_ups
from pylib.shared_patterns import SHARED
from pylib.util import FLAGS


# How far to look into the surrounding context to disambiguate the parse
LOOK_BACK_FAR = 40
LOOK_BACK_NEAR = 10

# These indicate that the parse is not really for an ear length
IS_ET = re.compile(r' e \.? t ', FLAGS)
IS_NUMBER = re.compile(' [#] ', FLAGS)
IS_MAG = re.compile(' magnemite ', FLAGS)
IS_ID = re.compile(' identifier | ident | id ', FLAGS)

# The 'E' abbreviation gets confused with abbreviation for East sometimes.
# Try to disambiguate the two by looking for a North near by.
LOOK_AROUND = 10
IS_EAST = re.compile(r' \b n ', FLAGS)


def fix_up(trait, text):
    """Fix problematic parses."""
    # Problem parses happen mostly with an ambiguous key
    if trait.ambiguous_key:

        # "E.T." is not an ear length measurement
        start = max(0, trait.start - LOOK_BACK_NEAR)
        if IS_ET.search(text, start, trait.start) \
                or IS_NUMBER.search(text, start, trait.start):
            return None

        # Magnemite confounds the abbreviation
        start = max(0, trait.start - LOOK_BACK_FAR)
        if IS_MAG.search(text, start, trait.start) \
                or IS_ID.search(text, start, trait.start):
            return None

        # Make sure it's not actually an abbreviation for "East"
        start = max(0, trait.start - LOOK_AROUND)
        end = min(len(text), trait.end + LOOK_AROUND)
        if IS_EAST.search(text, start, trait.start) \
                or IS_EAST.search(text, trait.end, end):
            return None

    # Try to disambiguate doubles quotes from inches
    return numeric_fix_ups(trait, text)


EAR_LENGTH = Base(
    name=__name__.split('.')[-1],
    fix_up=fix_up,

    scanners=[

        SHARED['uuid'],  # UUIDs cause problems with numbers

        # Units are in the key, like: EarLengthInMillimeters
        keyword('key_with_units', r"""
            ear \s* ( length | len ) \s* in \s* (?P<units> millimeters | mm )
            """),

        # Abbreviation containing the measured from notation, like: e/n or e/c
        fragment('char_measured_from', r"""
            (?<! [a-z] ) (?<! [a-z] \s )
            (?P<ambiguous_key> e ) /? (?P<measured_from1> n | c )
            (?! \.? [a-z] )
            """),

        # The abbreviation key, just: e. This can be a problem.
        fragment('char_key', r"""
            (?<! \w ) (?<! \w \s )
            (?P<ambiguous_key> e )
            (?! \.? \s? [a-z\(] )
            """),

        # Standard keywords that indicate an ear length follows
        keyword('keyword', [
            r' ear \s* from \s* (?P<measured_from1> notch | crown )',
            r' ear \s* ( length | len )',
            r' ear (?! \s* tag )',
            r' ef (?P<measured_from2> n | c )',
        ]),

        # Units
        SHARED['len_units'],

        # Fractional numbers, like: 9/16
        SHARED['fraction'],

        # Shorthand notation
        SHARED['shorthand_key'],
        SHARED['shorthand'],

        # Possible ranges of numbers like: "10 - 20" or just "10"
        SHARED['range'],

        # We allow random words in some situations
        keyword('word', r' ( [a-z] \w* ) '),

        # Some patterns require a separator
        fragment('sep', r' [;,] | $ '),
    ],

    replacers=[
        # Consider any of the following as just a key
        replacer('key', [
            'keyword',
            'char_key',
            'char_measured_from',
        ]),
    ],

    producers=[
        # Handle fractional values like: ear 9/16"
        producer(fraction, [

            # E.g.: ear = 9/16 in
            'key fraction (?P<units> len_units )',

            # Without units, like: ear = 9/16
            'key fraction',
        ]),

        # A typical ear length notation
        producer(simple, [

            # E.g.: earLengthInMM 9-10
            'key_with_units range',

            # E.g.: ear 9-10 mm
            'key range (?P<units> len_units )',

            # Missing units like: ear: 9-10
            'key range',
        ]),

        # Shorthand notation like: on tag: 11-22-33-44=99g
        producer(
            partial(shorthand_length, measurement='shorthand_el'), [
                'shorthand_key shorthand',  # With a key
                'shorthand',  # Without a key
            ]),
    ],
)
