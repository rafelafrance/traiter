"""Parse total length notations."""

from functools import partial
import regex
from pylib.stacked_regex.rule import fragment, keyword, producer
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.numeric import fix_up_inches, fraction, compound
from pylib.vertnet.numeric import shorthand_length, simple
from pylib.vertnet.shared_patterns import RULE
import pylib.vertnet.util as util


# How far to look into the surrounding context to disambiguate the parse
LOOK_BACK_FAR = 40
LOOK_BACK_NEAR = 10

# These indicate that the parse is not a total length
IS_ID = regex.compile(
    ' identifier | ident | id | collector ',
    util.FLAGS)
IS_TRAP = regex.compile(' trap ', util.FLAGS)
IS_TESTES = regex.compile(
    ' reproductive | gonad | test | scrotal | scrotum | scrot ',
    util.FLAGS)

# The 'L' abbreviation gets confused with abbreviation for Left sometimes.
# Try to disambiguate the two by looking for a Right near by.
LOOK_AROUND = 10
IS_LEFT = regex.compile(r' \b r \b ', util.FLAGS)


def fix_up(trait, text):
    """Fix problematic parses."""
    # Handle IDs
    start = max(0, trait.start - LOOK_BACK_FAR)
    if IS_ID.search(text, start, trait.start):
        return None

    # Handle traps, like: trap TL01
    start = max(0, trait.start - LOOK_BACK_NEAR)
    if IS_TRAP.search(text, start, trait.start):
        return None

    # Problem parses often happen with an ambiguous key
    if trait.ambiguous_key:

        # Testes measurement may involve an "L"
        start = max(0, trait.start - LOOK_AROUND)
        end = min(len(text), trait.end + LOOK_AROUND)
        if IS_TESTES.search(text, start, trait.start):
            return None

        # Make sure the "L" isn't for "left"
        if IS_LEFT.search(text, start, trait.start):
            return None
        if IS_LEFT.search(text, trait.end, end):
            return None

    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


TOTAL_LENGTH = Base(
    name=__name__.split('.')[-1],
    fix_up=fix_up,
    rules=[

        RULE['uuid'],  # UUIDs cause problems with numbers

        # Units are in the key, like: TotalLengthInMillimeters
        keyword('key_with_units', r"""
            ( total | snout \s* vent | head \s* body | fork ) \s*
            ( length | len )? \s* in \s* (?P<units> millimeters | mm )
            """),

        # Various total length keys
        fragment('key', [

            # E.g.: total-length-in
            r'total  [\s-]* length [\s-]* in',

            # E.g.: standardLengths
            r'( total | max | standard ) [\s-]* lengths? \b',

            # E.g.: Meas: length (L):
            r'meas [\s*:]? \s* length [\s(]* [l] [)\s:]*',

            # E.g.: measured: L
            r'meas ( [a-z]* )? \.? : \s* l (?! [a-z.] )',

            # E.g.: tol_
            r't [o.]? \s? l \.? \s? _? (?! [a-z.] )',

            # E.g.: s.l.
            r's \.? \s? l \.? (?! [a-z.] )',

            # E.g.: label length
            r'label [\s.]* lengths? \b',

            # E.g.: fork-length
            r'( fork | mean | body ) [\s-]* lengths? \b',

            # E.g.: s.v.l.
            r's \.? \s? v \.? \s? l \.? (?! [a-z.] )',

            # E.g.: snout-vent-length
            r'snout [\s-]* vent [\s-]* lengths? \b',
        ]),

        # Words that indicate we don't have a total length
        keyword('skip', 'horns?'),

        # The word length on its own. Make sure it isn't proceeded by a letter
        fragment('ambiguous', r'(?<! [a-z] )(?<! [a-z] \s ) lengths? '),

        # We don't know if this is a length until we see the units
        fragment('key_units_req', 'measurements? body total'.split()),

        # Units
        RULE['metric_len'],
        RULE['feet'],
        RULE['inches'],

        # Shorthand notation
        RULE['shorthand_key'],
        RULE['shorthand'],
        RULE['triple'],  # Truncated shorthand

        # Fractional numbers, like: 9/16
        RULE['fraction'],

        # Possible range of numbers like: "10 - 20" or just "10"
        RULE['range'],

        # The abbreviation key, just: t. This can be a problem.
        fragment('char_key', r' \b (?P<ambiguous_key> l ) (?= [:=-] ) '),

        # We allow random words in some situations
        keyword('word', r' ( [a-z] \w* ) '),

        # Some patterns require a separator
        fragment('semicolon', r' [;] | $ '),
        fragment('comma', r' [,] | $ '),

        # Handle fractional values like: total length 9/16"
        # E.g.: total = 9/16 inches
        producer(fraction, [
            'key_units_req fraction (?P<units> metric_len | feet | inches )']),

        # E.g.: svl 9/16 inches
        producer(fraction, [
            'key fraction (?P<units> metric_len | feet | inches )']),

        # E.g.: len 9/16 in
        producer(fraction, [
            """(?P<ambiguous_key> ambiguous) fraction
                (?P<units> metric_len | feet | inches )""",
            ]),

        # E.g.: total length 4 feet 7 inches
        producer(partial(compound, units=['ft', 'in']), [
            'key (?P<ft> range) feet comma? (?P<in> range) inches']),

        # E.g.: length 4 ft 7 in
        producer(partial(compound, units=['ft', 'in']), [
            """(?P<ambiguous_key>
                (?P<ft> range) feet comma? (?P<in> range) inches )""",
        ]),

        # A typical total length notation
        # E.g.: total length in mm 10 - 13
        producer(simple, 'key_with_units range'),

        # E.g.: tag 10-20-39 10 - 13 in
        producer(simple, [
            """shorthand_key triple? range
                (?P<units> metric_len | feet | inches )"""]),

        # E.g.: tag 10-20-39 cm 10-12
        producer(simple, [
            'shorthand_key triple? (?P<units> metric_len ) range']),

        # E.g.: total 10/20/30 10 to 12 cm
        producer(simple, [
            """key_units_req triple? range
                (?P<units> metric_len | feet | inches )"""]),

        # E.g.: 10 to 11 inches TL
        producer(simple, [
            'range (?P<units> metric_len | feet | inches ) key']),

        # E.g.: total 10-20-40 10 to 20 inches ToL
        producer(simple, [
            """ambiguous triple? range
                (?P<units> metric_len | feet | inches ) key"""]),

        # E.g.: total 10-20-40 10 to 20 ToL
        producer(simple, 'ambiguous triple? range key'),

        # E.g.: length 10 to 11 inches
        producer(simple, [
            """(?P<ambiguous_key> ambiguous) range
                (?P<units> metric_len | feet | inches )"""]),

        # E.g.: length feet 10 to 11
        producer(simple, [
            """(?P<ambiguous_key> ambiguous)
                (?P<units> metric_len | feet | inches ) range"""]),

        # E.g.: length 10 to 11
        producer(simple, '(?P<ambiguous_key> ambiguous) range'),

        # E.g.: SVL 10-11 cm
        producer(simple, 'key range (?P<units> metric_len | feet | inches )'),

        # E.g.: forkLen cm 10-11
        producer(simple, 'key (?P<units> metric_len | feet | inches ) range'),

        # E.g.: total length: 10-29-39 10-11
        producer(simple, 'key triple? range'),

        # E.g.: head body length is a whopping 12.4 meters
        producer(simple, [
            """key ( word | semicolon | comma ){1,3} range
                (?P<units> metric_len | feet | inches )"""]),

        # E.g.: SVL is 10-12
        producer(simple, 'key ( word | semicolon | comma ){1,3} range'),

        # E.g.: L 12.4 cm
        producer(simple, [
            'char_key range (?P<units> metric_len | feet | inches )']),

        # E.g.: L 12.4
        producer(simple, 'char_key range'),

        producer(
            partial(shorthand_length, measurement='shorthand_tl'), [
                '( shorthand_key | key_units_req ) shorthand',  # With a key
                'shorthand']),                                  # Without a key

        # Handle a truncated shorthand notation
        producer(
            partial(shorthand_length, measurement='shorthand_tl'), [
                '( shorthand_key | key_units_req ) shorthand',  # With a key
                'shorthand',                                    # Without a key
                """( shorthand_key | key_units_req ) triple
                    (?! shorthand | range )"""
            ]),
    ],
)
