"""Parse testes size notations."""

from stacked_regex.rule import fragment, keyword, producer, replacer
from pylib.shared_reproductive_patterns import REPRODUCTIVE
from pylib.shared_patterns import SHARED
from pylib.parsers.reproductive import double, convert
from pylib.parsers.base import Base


TESTES_SIZE = Base(
    name=__name__.split('.')[-1],
    scanners=[
        REPRODUCTIVE['testes'],

        # Note: abbrev differs from the one in the testes_state_trait
        keyword('abbrev', 'tes ts tnd td tns ta'.split()),

        # The abbreviation key, just: t. This can be a problem.
        fragment('char_key', r' \b t (?! [a-z] )'),

        REPRODUCTIVE['descended'],
        REPRODUCTIVE['scrotal'],
        REPRODUCTIVE['abdominal'],
        REPRODUCTIVE['size'],
        REPRODUCTIVE['other'],

        SHARED['uuid'],  # UUIDs cause problems with numeric traits

        REPRODUCTIVE['label'],
        REPRODUCTIVE['ambiguous_key'],
        REPRODUCTIVE['non'],
        REPRODUCTIVE['fully'],
        REPRODUCTIVE['partially'],
        SHARED['side'],
        SHARED['dim_side'],
        SHARED['dimension'],
        SHARED['cross'],
        SHARED['len_units'],
        REPRODUCTIVE['in'],
        REPRODUCTIVE['and'],
        REPRODUCTIVE['word'],
        REPRODUCTIVE['sep'],
    ],

    replacers=[
        replacer('state', [
            """(non | partially | fully )? descended """]
                 + """ scrotal abdominal size other """.split()),

        # A key with units, like: gonadLengthInMM
        replacer('key_with_units', r"""
            ambiguous_key dimension in (?P<units> len_units )
            """),

        # Male or female ambiguous, like: gonadLength1
        replacer('ambiguous', [
            # E.g.: GonadWidth2
            r' ambiguous_key dim_side',

            # E.g.: LeftGonadLength
            r' side ambiguous_key dimension ',

            # E.g.: Gonad Length
            r' ambiguous_key dimension ']),
    ],

    producers=[
        # These patterns contain measurements to both left & right testes
        # E.g.: reproductive data: tests left 10x5 mm, right 10x6 mm
        producer(double, [
            """label ( testes | abbrev | char_key )
                (?P<first> side cross )
                (?P<second> side cross )?"""]),

        # As above but without the testes marker:
        # E.g.: reproductive data: left 10x5 mm, right 10x6 mm
        producer(double, [
            """label
                (?P<first> side cross )
                (?P<second> side cross )?"""]),

        # Has the testes marker but is lacking the label
        # E.g.: testes left 10x5 mm, right 10x6 mm
        producer(double, [
            """( testes | abbrev | char_key )
                (?P<first> side cross )
                (?P<second> side cross )?"""]),

        # A typical testes size notation
        # E.g.: reproductive data: tests 10x5 mm
        producer(convert, 'label ( testes | abbrev | char_key ) cross'),

        # E.g.: reproductive data: left tests 10x5 mm
        producer(convert, 'label side ( testes | abbrev | char_key ) cross'),

        # E.g.: reproductive data: 10x5 mm
        producer(convert, 'label cross'),

        # May have a few words between the label and the measurement
        # E.g.: reproductive data=testes not descended - 6 mm
        producer(convert, [
            """label ( testes | abbrev | state | word | sep | char_key){0,3}
                ( testes | abbrev | state | char_key ) cross"""]),

        # Handles: gonadLengthInMM 4x3
        # And:     gonadLength 4x3
        producer(convert, '( key_with_units | ambiguous ) cross'),

        # E.g.: gonadLengthInMM 6 x 8
        producer(convert, [
            """( key_with_units | ambiguous )
                ( testes | abbrev | state | word | sep | char_key ){0,3}
                ( testes | abbrev | state | char_key ) cross"""]),

        # Anchored by testes but with words between
        # E.g.: testes scrotal; T = 9mm
        producer(convert, [
            """testes ( abbrev | state | word | sep | char_key ){0,3}
                ( abbrev | state | char_key ) cross"""]),

        # Anchored by testes but with only one word in between
        # E.g.: testes scrotal 9mm
        producer(convert, 'testes ( abbrev | state | word | char_key ) cross'),

        # E.g.: Testes 5 x 3
        producer(convert, '( testes | state | abbrev ) cross'),

        # E.g.: T 5 x 4
        producer(convert, '(?P<ambiguous_char> char_key ) cross'),
    ],
)
