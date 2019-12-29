"""Parse hind foot length notations."""

from functools import partial
from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.numeric import fix_up_inches, shorthand_length
from pylib.vertnet.numeric import fraction, simple
import pylib.vertnet.shared_patterns as patterns

CATALOG = RuleCatalog(patterns.CATALOG)


def fix_up(trait, text):
    """Fix problematic parses."""
    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


HIND_FOOT_LENGTH = Base(
    name=__name__.split('.')[-1],
    rules=[
        CATALOG['uuid'],  # UUIDs cause problems with numbers

        # Units are in the key, like: HindFootLengthInMillimeters
        CATALOG.term(
            'key_with_units',
            r"""( hind \s* )? foot \s* ( length | len ) \s* in \s*
                    (?P<units> millimeters | mm )"""),

        # Standard keywords that indicate a hind foot length follows
        CATALOG.term('key', [
            r'hind \s* foot \s* with \s* (?P<includes> claw )',
            r'hind \s* foot ( \s* ( length | len ) )?',
            'hfl | hf']),

        # Some patterns require a separator
        CATALOG.part('sep', r' [;,] | $ ', capture=False),

        CATALOG.grouper('noise', ' word dash '.split()),

        # Handle fractional values like: hindFoot 9/16"
        CATALOG.producer(fraction, [
            'key len_fraction units',   # E.g.: hindFoot = 9/16 inches
            'key len_fraction',         # E.g.: hindFoot = 9/16
            ]),

        # A typical hind-foot notation
        CATALOG.producer(simple, [
            'key_with_units len_range',     # E.g.: hindFootLengthInMM=9-10
            'key noise? len_range units ',  # E.g.: hindFootLength=9-10 mm
            'key noise? len_range', # Missing units like: hindFootLength 9-10
            'key dash number units',
        ]),

        CATALOG.producer(partial(
            shorthand_length,
            measurement='shorthand_hfl'), [
                'shorthand_key shorthand',  # With a key
                'shorthand',                # Without a key
                # Handle a truncated shorthand notation
                'shorthand_key triple (?! shorthand | len_range )']),
    ],
)
