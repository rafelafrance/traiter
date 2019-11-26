"""Parse ovaries size notations."""

from pylib.stacked_regex.rule import producer, grouper
from pylib.vertnet.shared_reproductive_patterns import RULE
from pylib.vertnet.reproductive import double, convert
from pylib.vertnet.parsers.base import Base


OVARY_SIZE = Base(
    name=__name__.split('.')[-1],
    rules=[
        RULE['ovary'],
        RULE['other'],
        RULE['horns'],
        RULE['covered'],
        RULE['fat'],
        RULE['developed'],
        RULE['visible'],
        RULE['destroyed'],
        RULE['mature'],
        RULE['uterus'],
        RULE['fallopian'],
        RULE['active'],
        RULE['lut'],
        RULE['corpus'],
        RULE['alb'],
        RULE['nipple'],
        RULE['comma'],
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
        RULE['in'],
        RULE['and'],
        RULE['word'],
        RULE['sep'],

        # A key with units, like: gonadLengthInMM
        grouper('key_with_units', r"""
            ambiguous_key dimension in (?P<units> len_units )
            """),

        # E.g.: active
        # Or:   immature
        grouper('state', 'active mature destroyed visible developed'.split()),

        # Male or female ambiguous, like: gonadLength1
        grouper('ambiguous', """
            ambiguous_key dim_side
            | side ambiguous_key dimension
            | ambiguous_key dimension """),

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
        producer(convert, 'side? ovary ( state | word ) cross'),

        # E.g.: Ovaries 5 x 3
        producer(convert, 'side? ovary cross'),
    ],
)
