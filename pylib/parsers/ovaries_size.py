"""Parse ovaries size notations."""

from stacked_regex.rule import fragment, producer, replacer
from pylib.shared_reproductive_patterns import REPRODUCTIVE
from pylib.shared_patterns import SHARED
from pylib.parsers.reproductive import double, convert
from pylib.parsers.base import Base


OVARY_SIZE = Base(
    name=__name__.split('.')[-1],
    scanners=[
        REPRODUCTIVE['ovary'],
        REPRODUCTIVE['other'],
        REPRODUCTIVE['horns'],
        REPRODUCTIVE['covered'],
        REPRODUCTIVE['fat'],
        REPRODUCTIVE['developed'],
        REPRODUCTIVE['visible'],
        REPRODUCTIVE['destroyed'],
        REPRODUCTIVE['mature'],
        REPRODUCTIVE['uterus'],
        REPRODUCTIVE['fallopian'],
        REPRODUCTIVE['active'],
        REPRODUCTIVE['lut'],
        REPRODUCTIVE['corpus'],
        REPRODUCTIVE['alb'],
        REPRODUCTIVE['nipple'],

        # Commas are sometimes separators & other times punctuation
        fragment('comma', r'[,]'),

        REPRODUCTIVE['label'],
        REPRODUCTIVE['ambiguous_key'],
        REPRODUCTIVE['non'],
        REPRODUCTIVE['fully'],
        REPRODUCTIVE['partially'],
        SHARED['side_cross'],
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
        # A key with units, like: gonadLengthInMM
        replacer('key_with_units', r"""
            ambiguous_key dimension in (?P<units> len_units )
            """),

        # E.g.: active
        # Or:   immature
        replacer('state', 'active mature destroyed visible developed'.split()),

        # Male or female ambiguous, like: gonadLength1
        replacer('ambiguous', """
            ambiguous_key dim_side
            | side ambiguous_key dimension
            | ambiguous_key dimension """),
    ],

    producers=[
        # These patterns contain measurements to both left & right ovaries
        # E.g.: reproductive data: ovaries left 10x5 mm, right 10x6 mm
        producer(double, """ label ovary side_cross """),

        # As above but without the ovaries marker:
        # E.g.: reproductive data: left 10x5 mm, right 10x6 mm
        producer(double, """label side_cross"""),

        # Has side before gonad key
        # E.g.: left ovary: 4 x 2 mm
        producer(double, """ side_cross """),

        # Has the ovaries marker but is lacking the label
        # E.g.: ovaries left 10x5 mm, right 10x6 mm
        producer(double, """ ovary side_cross """),

        # A typical testes size notation
        # E.g.: reproductive data: ovaries 10x5 mm
        producer(convert, ' label ovary cross '),

        # E.g.: reproductive data: left ovaries 10x5 mm
        producer(convert, ' label side ovary cross '),

        # E.g.: left ovaries 10x5 mm
        producer(convert, ' side ovary cross '),

        # E.g.: reproductive data: 10x5 mm
        producer(convert, 'label cross'),

        # May have a few words between the label and the measurement
        producer(convert, """
            label ( ovary | state | word | sep ){0,3}
            ( ovary | state ) cross"""),

        # Handles: gonadLengthInMM 4x3
        # And:     gonadLength 4x3
        producer(convert, '( key_with_units | ambiguous ) cross'),

        # E.g.: gonadLengthInMM 6 x 8
        producer(convert, """
            ( key_with_units | ambiguous )
            ( ovary | state | word | sep ){0,3}
            ( ovary | state ) cross"""),

        # Anchored by ovaries but with words between
        producer(convert, 'ovary ( state | word | sep ){0,3} state cross'),

        # Anchored by ovaries but with only one word in between
        # E.g.: ovaries scrotal 9mm
        producer(convert, 'ovary ( state | word ) cross'),

        # E.g.: Ovaries 5 x 3
        producer(convert, 'ovary cross'),
    ],
)
