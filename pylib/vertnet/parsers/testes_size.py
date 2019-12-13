"""Parse testes size notations."""

from pylib.stacked_regex.rule import frag, vocab, producer, grouper
from pylib.vertnet.shared_reproductive_patterns import RULE
from pylib.vertnet.reproductive import double, convert
from pylib.vertnet.parsers.base import Base


TESTES_SIZE = Base(
    name=__name__.split('.')[-1],
    rules=[
        RULE['testes'],

        # Note: abbrev differs from the one in the testes_state_trait
        vocab('abbrev', 'tes ts tnd td tns ta'.split()),

        # The abbreviation key, just: t. This can be a problem.
        frag('char_key', r' \b t (?! [a-z] )'),

        # A key with units, like: gonadLengthInMM
        vocab('key_with_units', r"""
            (?P<ambiguous_key> gonad ) \s*
                (?P<dim> length | len | width ) \s* in \s*
                (?P<len_units> millimeters | mm )
            """),

        RULE['descended'],
        RULE['scrotal'],
        RULE['abdominal'],
        RULE['size'],
        RULE['other'],

        RULE['uuid'],  # UUIDs cause problems with numeric traits

        RULE['label'],
        RULE['ambiguous_key'],
        RULE['non'],
        RULE['fully'],
        RULE['partially'],
        RULE['side_cross_set'],
        RULE['side'],
        RULE['dim_side'],
        RULE['dimension'],
        RULE['cross_set'],
        RULE['range_set'],
        RULE['in'],
        RULE['pounds'],
        RULE['ounces'],
        RULE['metric_mass'],
        RULE['mass_units'],
        RULE['word'],
        RULE['sep'],

        grouper('value', """
            cross | number len_units? (?! mass_units ) """),

        grouper('state', [
            """(non | partially | fully )? descended """]
                + """ scrotal abdominal size other """.split()),

        # Male or female ambiguous, like: gonadLength1
        grouper('ambiguous', """
            ambiguous_key dim_side
            | side ambiguous_key dimension
            | ambiguous_key dimension """),

        # These patterns contain measurements to both left & right testes
        # E.g.: reproductive data: tests left 10x5 mm, right 10x6 mm
        producer(
            double, """label ( testes | abbrev | char_key ) side_cross """),

        # As above but without the testes marker:
        # E.g.: reproductive data: left 10x5 mm, right 10x6 mm
        producer(double, """ label side_cross """),

        # Has the testes marker but is lacking the label
        # E.g.: testes left 10x5 mm, right 10x6 mm
        producer(double, """( testes | abbrev | char_key ) side_cross """),

        # E.g.: reproductive data: left 10x5 mm
        producer(double, """
            label
                (?P<side_1> side ) (?P<value_1> number )
                    (?P<units_1> len_units )?
                (?P<side_2> side ) (?P<value_2> number )
                    (?P<units_2> len_units )? """),

        # E.g.: reproductive data: left 10x5 mm
        producer(convert, """
            ( testes | abbrev | char_key )
                (?P<value_1> number ) (?P<units_1> len_units )?
                dash
                (?P<value_2> number ) (?P<units_2> len_units )? """),

        # A typical testes size notation
        # E.g.: reproductive data: tests 10x5 mm
        producer(convert, 'label ( testes | abbrev | char_key ) side_cross'),

        # E.g.: reproductive data: left tests 10x5 mm
        producer(convert, """
            label side ( testes | abbrev | char_key )
                (dash | comma)? value"""),

        # E.g.: reproductive data=T: L-2x4mm
        producer(convert, """
            label ( testes | abbrev | char_key ) side dash? value """),

        # E.g.: reproductive data: left 10x5 mm
        producer(convert, 'label side dash? value len_units?'),

        # E.g.: reproductive data: 10x5 mm
        producer(convert, 'label value len_units?'),

        # Has the testes marker but is lacking the label
        # E.g.: testes left 10x5 mm, right 10x6 mm
        producer(convert, """( testes | abbrev ) value """),

        # May have a few words between the label and the measurement
        # E.g.: reproductive data=testes not descended - 6 mm
        producer(convert, [
            """label ( testes | abbrev | state | word | sep | char_key){0,3}
                ( testes | abbrev | state | char_key )
                ( dash | comma )? value"""]),

        # Handles: gonadLengthInMM 4x3
        # And:     gonadLength 4x3
        producer(convert, '( ambiguous | key_with_units ) value'),

        # E.g.: gonadLengthInMM 6 x 8
        producer(convert, [
            """( key_with_units | ambiguous )
                ( testes | abbrev | state | word | sep | char_key ){0,3}
                ( testes | abbrev | state | char_key ) value"""]),

        # Anchored by testes but with words between
        # E.g.: testes scrotal; T = 9mm
        producer(convert, [
            """testes ( abbrev | state | word | sep | char_key ){0,3}
                ( abbrev | state | char_key ) value"""]),

        # Anchored by testes but with only one word in between
        # E.g.: testes scrotal 9mm
        producer(convert, """testes ( abbrev | state | word | char_key )
                    ( comma | dash )? value"""),

        # E.g.: Testes 5 x 3
        producer(convert, """
            ( testes | state | abbrev ) (comma | dash | x )? value """),

        # E.g.: T 5 x 4
        producer(convert, '(?P<ambiguous_char> char_key ) value'),
    ],
)
