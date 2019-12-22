"""Parse tail length notations."""

from functools import partial
import regex
from pylib.shared.util import FLAGS
from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.numeric import fix_up_inches, shorthand_length
from pylib.vertnet.numeric import simple, fraction
import pylib.vertnet.shared_patterns as patterns

CATALOG = RuleCatalog(patterns.CATALOG)

# How far to look into the surrounding context to disambiguate the parse
LOOK_BACK_FAR = 40
LOOK_BACK_NEAR = 20

# These indicate that the parse is not really for a tail length
IS_TESTES = regex.compile(
    ' reproductive | gonad | test | scrotal | scrotum | scrot ',
    FLAGS)
IS_ELEVATION = regex.compile(' elevation | elev ', FLAGS)
IS_TOTAL = regex.compile(' body | nose | snout ', FLAGS)
IS_TAG = regex.compile(' tag ', FLAGS)
IS_ID = regex.compile(' identifier | ident | id ', FLAGS)


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
        if (IS_TESTES.search(text, start, trait.start)
                or IS_ELEVATION.search(text, start, trait.start)
                or IS_ID.search(text, start, trait.start)):
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
    rules=[
        CATALOG['uuid'],  # UUIDs cause problems with numbers

        # Looking for keys like: tailLengthInMM
        CATALOG.term('key_with_units', r"""
            tail \s* ( length | len ) \s* in \s*
            (?P<units> millimeters | mm ) """),

        # The abbreviation key, just: t. This can be a problem.
        CATALOG.part('char_key', r"""
            \b (?P<ambiguous_key> t ) (?! [a-z] ) (?! _ \D )
            """),

        # Standard keywords that indicate a tail length follows
        CATALOG.term('keyword', [
            r' tail \s* length ',
            r' tail \s* len ',
            'tail',
            'tal']),

        # Some patterns require a separator
        CATALOG.part('sep', r' [;,] | $ ', capture=False),

        # Consider all of these tokens a key
        CATALOG.grouper('key', 'keyword char_key'.split()),

        # Handle fractional values like: tailLength 9/16"
        CATALOG.producer(fraction, [

            # E.g.: tail = 9/16 in
            'key fraction (?P<units> len_units )',

            # Without units, like: tail = 9/16
            'key fraction']),

        # A typical tail length notation
        CATALOG.producer(simple, [

            # E.g.: tailLengthInMM=9-10
            'key_with_units range',

            # E.g.: tailLength=9-10 mm
            'key range (?P<units> len_units )',

            # Missing units like: tailLength 9-10
            'key range',
        ]),

        CATALOG.producer(
            partial(shorthand_length, measurement='shorthand_tal'), [
                'shorthand_key shorthand',  # With a key
                'shorthand',  # Without a key
                # Handle a truncated shorthand notation
                'shorthand_key triple (?! shorthand | range )']),
    ],
)
