"""Parse embryo lengths."""

from stacked_regex.rule import fragment, keyword, producer, replacer
from pylib.numeric_trait import NumericTrait
from pylib.parsers.numeric import fix_up_inches
from pylib.parsers.base import Base
from pylib.shared_patterns import SHARED
from pylib.shared_reproductive_patterns import REPRODUCTIVE


def convert(token):
    """Convert parsed token into a trait product."""
    trait = NumericTrait(start=token.start, end=token.end)
    trait.cross_value(token)
    return trait


def fix_up(trait, text):
    """Fix problematic parses."""
    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


EMBRYO_LENGTH = Base(
    fix_up=fix_up,

    scanners=[
        SHARED['uuid'],  # UUIDs cause problems with numbers

        REPRODUCTIVE['embryo'],

        keyword('crown_rump', r"""
            (?<! collector [\s=:.] ) (?<! reg [\s=:.] ) (
                ( crown | cr ) ( [_\s\-] | \s+ to \s+ )? rump
                | (?<! [a-z] ) crl (?! [a-z] )
                | (?<! [a-z] ) cr  (?! [a-z] )
            )"""),

        keyword('length', r' length | len '),

        keyword('prep', ' of from '.split()),
        keyword('side', r""" left | right | lf | lt | rt | [lr] """),

        SHARED['len_units'],

        SHARED['cross'],
        fragment('cross_joiner', SHARED['cross_joiner'].pattern),

        fragment('word', r' \w+ '),
        fragment('separator', r' [;"?/] '),
    ],

    replacers=[
        replacer('skip', ' prep word cross '),
        replacer('measurement', ' (cross_joiner)? cross '),
    ],

    producers=[
        producer(convert, [
            # E.g.: crown-rump length=13 mm
            """ (embryo)? crown_rump (length)?
                measurement (?P<units> len_units )? """,
        ]),

        producer(convert, [
            # E.g.: 15 mm, crown-rump length
            """ (embryo)? measurement (?P<units> len_units )?
                crown_rump (length)? """,
        ]),
    ],
)
