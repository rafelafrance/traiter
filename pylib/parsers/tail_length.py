"""Parse tail length notations."""

import re
from functools import partial
from stacked_regex.rule import fragment, keyword, producer, replacer
from pylib.parsers.base import Base
from pylib.parsers.numeric import fix_up_inches, shorthand_length, fraction
from pylib.parsers.numeric import simple
from pylib.shared_patterns import SHARED
import pylib.util as util


# How far to look into the surrounding context to disambiguate the parse
LOOK_BACK_FAR = 40
LOOK_BACK_NEAR = 20

# These indicate that the parse is not really for a tail length
IS_TESTES = re.compile(
    ' reproductive | gonad | test | scrotal | scrotum | scrot ',
    util.FLAGS)
IS_ELEVATION = re.compile(' elevation | elev ', util.FLAGS)
IS_TOTAL = re.compile(' body | nose | snout ', util.FLAGS)
IS_TAG = re.compile(' tag ', util.FLAGS)
IS_ID = re.compile(' identifier | ident | id ', util.FLAGS)


def fix_up(trait, text):
    """Fix problematic parses."""
    # Check that this isn't a total length trait
    start = max(0, trait.start - LOOK_BACK_NEAR)
    if IS_TOTAL.search(text, start, trait.start):
        return None

    # Problem parses happen mostly with an ambiguous key
    if trait.ambiguous_key:

        # Make sure this isn't a testes measurement
        start = max(0, trait.start - LOOK_BACK_FAR)
        if IS_TESTES.search(text, start, trait.start) \
                or IS_ELEVATION.search(text, start, trait.start) \
                or IS_ID.search(text, start, trait.start):
            return None

        # Make sure this isn't a tag
        start = max(0, trait.start - LOOK_BACK_NEAR)
        if IS_TAG.search(text, start, trait.start):
            return None

    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


TAIL_LENGTH = Base(
    name=__name__.split('.')[-1],
    fix_up=fix_up,
    scanners=[
        SHARED['uuid'],  # UUIDs cause problems with numbers

        # Looking for keys like: tailLengthInMM
        keyword('key_with_units', r"""
            tail \s* ( length | len ) \s* in \s*
            (?P<units> millimeters | mm ) """),

        # The abbreviation key, just: t. This can be a problem.
        fragment('char_key', r"""
            \b (?P<ambiguous_key> t ) (?! [a-z] ) (?! _ \D )
            """),

        # Standard keywords that indicate a tail length follows
        keyword('keyword', [
            r' tail \s* length ',
            r' tail \s* len ',
            'tail',
            'tal']),

        # Units
        SHARED['len_units'],

        # Shorthand notation
        SHARED['shorthand_key'],
        SHARED['shorthand'],

        # Fractional numbers, like: 9/16
        SHARED['fraction'],

        # Possible pairs of numbers like: "10 - 20" or just "10"
        SHARED['range'],

        # Sometimes the last number is missing in the shorthand notation
        SHARED['triple'],

        # We allow random words in some situations
        keyword('word', r' ( [a-z] \w* ) '),

        # Some patterns require a separator
        fragment('sep', r' [;,] | $ '),
    ],

    replacers=[
        # Consider all of these tokens a key
        replacer('key', 'keyword char_key'.split()),
    ],

    producers=[
        # Handle fractional values like: tailLength 9/16"
        producer(fraction, [

            # E.g.: tail = 9/16 in
            'key fraction (?P<units> len_units )',

            # Without units, like: tail = 9/16
            'key fraction']),

        # A typical tail length notation
        producer(simple, [

            # E.g.: tailLengthInMM=9-10
            'key_with_units range',

            # E.g.: tailLength=9-10 mm
            'key range (?P<units> len_units )',

            # Missing units like: tailLength 9-10
            'key range',
        ]),

        producer(
            partial(shorthand_length, measurement='shorthand_tal'), [
                'shorthand_key shorthand',  # With a key
                'shorthand',  # Without a key
                # Handle a truncated shorthand notation
                'shorthand_key triple (?! shorthand | range )']),
    ],
)
