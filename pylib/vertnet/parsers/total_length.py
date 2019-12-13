"""Parse total length notations."""

from functools import partial
import regex
from pylib.shared.util import FLAGS
from pylib.stacked_regex.rule import part, term, grouper, producer
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
    if ambiguous_key_problem(trait, text):
        return None

    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


def ambiguous_key_problem(trait, text):
    """Fix problems occurring with ambiguous keys."""
    if trait.ambiguous_key:
        start = max(0, trait.start - LOOK_AROUND)
        end = min(len(text), trait.end + LOOK_AROUND)

        # Testes measurement may involve an "L"
        if IS_TESTES.search(text, start, trait.start):
            return True

        # Make sure the "L" isn't for "left"
        if IS_LEFT.search(text, start, trait.start):
            return True
        if IS_LEFT.search(text, trait.end, end):
            return True

    return False


TOTAL_LENGTH = Base(
    name=__name__.split('.')[-1],
    fix_up=fix_up,
    rules=[
        RULE['uuid'],  # UUIDs cause problems with numbers

        # Units are in the key, like: TotalLengthInMillimeters
        term('key_with_units', r"""
            ( total | snout \s* vent | head \s* body | fork ) \s*
            ( length | len )? \s* in \s* (?P<units> millimeters | mm )
            """),

        # Various total length keys
        part('len_key', r"""
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
        term('skip', ' horns? tag '.split()),

        # The word length on its own. Make sure it isn't proceeded by a letter
        part('ambiguous', r"""
            (?<! [a-z] \s* ) (?P<ambiguous_key> lengths? ) """),

        # # We don't know if this is a length until we see the units
        part('key_units_req', 'measurements? body total'.split()),

        # # Shorthand notation
        RULE['shorthand_key'],
        RULE['shorthand'],
        RULE['triple'],  # Truncated shorthand

        # Fractional numbers, like: 9/16
        RULE['len_fraction'],

        # Possible range of numbers like: "10 - 20" or just "10"
        RULE['len_range'],

        # compound length like 2 ft 3.1 - 4.5 in
        RULE['compound_len'],

        # The abbreviation key, just: t. This can be a problem.
        part('char_key', r' \b (?P<ambiguous_key> l ) (?= [:=-] ) '),

        # We allow random words in some situations
        RULE['eq'],

        # # Some patterns require a separator
        part('semicolon', r' [;] | $ '),
        part('comma', r' [,] | $ '),

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

        # E.g.: total length: 10-29-39 10-11
        producer(simple, '( key | key_units_req ) triple? len_range'),

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
