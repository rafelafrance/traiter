"""Parse hind foot length notations."""

from functools import partial
from stacked_regex.rule import fragment, keyword, producer
from pylib.parsers.base import Base
from pylib.parsers.numeric import fix_up_inches, shorthand_length, fraction
from pylib.parsers.numeric import simple
from pylib.shared_patterns import SHARED


def fix_up(trait, text):
    """Fix problematic parses."""
    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


HIND_FOOT_LENGTH = Base(
    scanners=[
        SHARED['uuid'],  # UUIDs cause problems with numbers

        # Units are in the key, like: HindFootLengthInMillimeters
        keyword(
            'key_with_units',
            r"""( hind \s* )? foot \s* ( length | len ) \s* in \s*
                    (?P<units> millimeters | mm )"""),

        # Standard keywords that indicate a hind foot length follows
        keyword('key', [
            r'hind \s* foot \s* with \s* (?P<includes> claw )',
            r'hind \s* foot ( \s* ( length | len ) )?',
            'hfl | hf']),

        # Units
        SHARED['len_units'],

        # Shorthand notation
        SHARED['shorthand_key'],
        SHARED['shorthand'],

        # Fractional numbers, like: 9/16
        SHARED['fraction'],

        # Possible range of numbers like: "10 - 20" or just "10"
        SHARED['range'],

        # Sometimes the last number is missing in the shorthand notation
        SHARED['triple'],

        # We allow random words in some situations
        keyword('word', r' ( [a-z] \w* ) '),

        # Some patterns require a separator
        fragment('sep', r' [;,] | $ '),

    ],

    replacers=[
    ],

    producers=[
        # Handle fractional values like: hindFoot 9/16"
        producer(fraction, [

            # E.g.: hindFoot = 9/16 inches
            'key fraction (?P<units> len_units )',

            # E.g.: hindFoot = 9/16
            'key fraction']),

        # A typical hind-foot notation
        producer(simple, [

            # E.g.: hindFootLengthInMM=9-10
            'key_with_units range',

            # E.g.: hindFootLength=9-10 mm
            'key range (?P<units> len_units )',

            # Missing units like: hindFootLength 9-10
            'key range']),

        producer(partial(
            shorthand_length, measurement='shorthand_hfl'), [
                'shorthand_key shorthand',  # With a key
                'shorthand',                # Without a key
                # Handle a truncated shorthand notation
                'shorthand_key triple (?! shorthand | range )']),
    ],
)
