"""Parse hind foot length notations."""

from functools import partial
from pylib.stacked_regex.rule import frag, vocab, grouper, producer
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.numeric import fix_up_inches, shorthand_length
from pylib.vertnet.numeric import fraction, simple
from pylib.vertnet.shared_patterns import RULE


def fix_up(trait, text):
    """Fix problematic parses."""
    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


HIND_FOOT_LENGTH = Base(
    name=__name__.split('.')[-1],
    rules=[
        RULE['uuid'],  # UUIDs cause problems with numbers

        # Units are in the key, like: HindFootLengthInMillimeters
        vocab(
            'key_with_units',
            r"""( hind \s* )? foot \s* ( length | len ) \s* in \s*
                    (?P<units> millimeters | mm )"""),

        # Standard keywords that indicate a hind foot length follows
        vocab('key', [
            r'hind \s* foot \s* with \s* (?P<includes> claw )',
            r'hind \s* foot ( \s* ( length | len ) )?',
            'hfl | hf']),

        # Shorthand notation
        RULE['shorthand_key'],
        RULE['shorthand'],

        # Fractional numbers, like: 9/16
        RULE['fraction_set'],

        # Possible range of numbers like: "10 - 20" or just "10"
        RULE['range_set'],

        # Sometimes the last number is missing in the shorthand notation
        RULE['triple'],

        # We allow random words in some situations
        vocab('word', r' ( [a-z] \w* ) ', capture=False),

        # Some patterns require a separator
        frag('sep', r' [;,] | $ ', capture=False),

        grouper('noise', ' word dash '.split()),

        # Handle fractional values like: hindFoot 9/16"
        producer(fraction, [

            # E.g.: hindFoot = 9/16 inches
            'key fraction units',

            # E.g.: hindFoot = 9/16
            'key fraction']),

        # A typical hind-foot notation
        producer(simple, [

            # E.g.: hindFootLengthInMM=9-10
            'key_with_units range',

            # E.g.: hindFootLength=9-10 mm
            'key noise? range units ',

            # Missing units like: hindFootLength 9-10
            'key noise? range',

            'key dash number units',
        ]),

        producer(partial(
            shorthand_length, measurement='shorthand_hfl'), [
                'shorthand_key shorthand',  # With a key
                'shorthand',                # Without a key
                # Handle a truncated shorthand notation
                'shorthand_key triple (?! shorthand | range )']),
    ],
)
