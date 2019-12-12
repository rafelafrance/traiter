"""Parse total length notations."""

from functools import partial
import regex
from pylib.shared.util import FLAGS
from pylib.stacked_regex.rule import fragment, keyword, grouper, producer
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.numeric import fix_up_inches, fraction, compound
import pylib.vertnet.numeric as numeric
from pylib.vertnet.shared_patterns import RULE


# How far to look into the surrounding context to disambiguate the parse
LOOK_BACK_FAR = 40
LOOK_BACK_NEAR = 10

# These indicate that the parse is not a total length
IS_ID = regex.compile(' identifier | ident | id | collector ', FLAGS)
IS_TRAP = regex.compile(' trap ', FLAGS)
IS_TESTES = regex.compile(
    ' reproductive | gonad | test | scrotal | scrotum | scrot ', FLAGS)

# The 'L' abbreviation gets confused with abbreviation for Left sometimes.
# Try to disambiguate the two by looking for a Right near by.
LOOK_AROUND = 10
IS_LEFT = regex.compile(r' \b r \b ', FLAGS)


def simple(token):
    """Post-process the simple parser."""
    trait = numeric.simple(token)
    if trait.ambiguous_key and token.groups.get('len_key'):
        delattr(trait, 'ambiguous_key')
    return trait


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
        fragment('len_key', r"""
            t \s* [o.]? \s* l [._]? (?! [a-z] )
            | total  [\s-]* length [\s-]* in
            | ( total | max | standard ) [\s-]* lengths? \b
            | meas [\s*:]? \s* length [\s(]* [l] [)\s:]*
            | meas ( [a-z]* )? \.? : \s* l (?! [a-z.] )
            | s \.? \s? l \.? (?! [a-z.] )
            | label [\s.]* lengths? \b
            | ( fork | mean | body ) [\s-]* lengths? \b
            | s \.? \s? v \.? \s? l \.? (?! [a-z.] )
            | snout [\s-]* vent [\s-]* lengths? \b
            """),

        # Words that indicate we don't have a total length
        keyword('skip', ' horns? tag '.split()),

        # The word length on its own. Make sure it isn't proceeded by a letter
        fragment('ambiguous', r"""
            (?<! [a-z] \s* ) (?P<ambiguous_key> lengths? ) """),

        # # We don't know if this is a length until we see the units
        fragment('key_units_req', 'measurements? body total'.split()),

        # # Shorthand notation
        RULE['shorthand_key'],
        RULE['shorthand'],
        RULE['triple'],  # Truncated shorthand

        # Fractional numbers, like: 9/16
        RULE['len_fraction_set'],

        # Possible range of numbers like: "10 - 20" or just "10"
        RULE['len_range_set'],

        # compound length like 2 ft 3.1 - 4.5 in
        RULE['compound_len_set'],

        # The abbreviation key, just: t. This can be a problem.
        fragment('char_key', r' \b (?P<ambiguous_key> l ) (?= [:=-] ) '),

        # We allow random words in some situations
        # keyword('word', r' [a-z] \w* '),
        RULE['eq'],

        # # Some patterns require a separator
        fragment('semicolon', r' [;] | $ '),
        fragment('comma', r' [,] | $ '),

        grouper('key', """
            ( key_with_units | len_key | shorthand_key | ambiguous
                | char_key )
            ( eq | dash )? """),

        grouper('value', """ len_range | number (?P<units> len_units )? """),
        grouper('value_units', """\
            len_range | number (?P<units> len_units ) """),

        # E.g.: 10 to 11 inches TL
        producer(simple, 'value (?P<units> len_units ) key'),
        producer(simple, """ key value key? """),
        producer(simple, """ key (?P<units> len_units ) value """),
        producer(simple, """ key_units_req value_units """),

        # E.g.: total length 4 feet 7 inches
        producer(compound, ' key? compound_len '),

        # Handle fractional values like: total length 9/16"
        # E.g.: total = 9/16 inches
        producer(fraction, [
            'key_units_req len_fraction (?P<units> len_units )']),

        # E.g.: svl 9/16 inches
        producer(fraction, [
            'key len_fraction (?P<units> len_units )']),

        # E.g.: len 9/16 in
        producer(fraction, """
            (?P<ambiguous_key> ambiguous) len_fraction
                (?P<units> len_units )"""),

        # A typical total length notation
        # E.g.: total length in mm 10 - 13
        # producer(simple, '( key_with_units | shorthand_key ) range'),

        # E.g.: tag 10-20-39 10 - 13 in
        # producer(simple, [
        #     """shorthand_key triple? range
        #         (?P<units> len_units )"""]),

        # E.g.: tag 10-20-39 cm 10-12
        # producer(simple, [
        #     'shorthand_key triple? (?P<units> metric_len ) range']),

        # E.g.: total 10/20/30 10 to 12 cm
        # producer(simple, [
        #     """key_units_req triple? range
        #         (?P<units> len_units )"""]),

        # E.g.: total 10-20-40 10 to 20 inches ToL
        # producer(simple, [
        #     """ambiguous triple? range
        #         (?P<units> len_units ) key"""]),

        # E.g.: total 10-20-40 10 to 20 ToL
        # producer(simple, 'ambiguous triple? range key'),

        # E.g.: length 10 to 11 inches
        # producer(simple, [
        #     """(?P<ambiguous_key> ambiguous) range
        #         (?P<units> len_units )"""]),

        # E.g.: length feet 10 to 11
        # producer(simple, [
        #     """(?P<ambiguous_key> ambiguous)
        #         (?P<units> len_units ) range"""]),

        # E.g.: length 10 to 11
        # producer(simple, '(?P<ambiguous_key> ambiguous) range'),

        # E.g.: SVL 10-11 cm
        # producer(simple, 'key range (?P<units> len_units )'),

        # E.g.: forkLen cm 10-11
        # producer(simple, 'key (?P<units> len_units ) range'),

        # E.g.: total length: 10-29-39 10-11
        producer(simple, '( key | key_units_req ) triple? len_range'),

        # E.g.: head body length is a whopping 12.4 meters
        # producer(simple, [
        #     """key ( word | semicolon | comma ){1,3} range
        #         (?P<units> len_units )"""]),

        # E.g.: SVL is 10-12
        # producer(simple, 'key ( word | semicolon | comma ){1,3} range'),

        # E.g.: L 12.4 cm
        producer(simple, """
            char_key value (?P<units> len_units )? """),

        producer(
            partial(numeric.shorthand_length, measurement='shorthand_tl'), [
                '( key | key_units_req ) shorthand',  # With a key
                'shorthand']),                        # Without a key

        # Handle a truncated shorthand notation
        producer(
            partial(numeric.shorthand_length, measurement='shorthand_tl'), [
                'key shorthand',  # With a key
                'shorthand',      # Without a key
                """ ( key | key_units_req ) triple
                    (?! shorthand | len_range )"""
            ]),
    ],
)
