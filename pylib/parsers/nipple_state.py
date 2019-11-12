"""Parse nipple state notations."""

from stacked_regex.rule import fragment, keyword, producer, replacer
from pylib.parsers.base import Base, convert
from pylib.shared_reproductive_patterns import REPRODUCTIVE


NIPPLE_STATE = Base(
    name=__name__.split('.')[-1],
    scanners=[
        REPRODUCTIVE['size'],
        REPRODUCTIVE['fully'],
        REPRODUCTIVE['partially'],
        REPRODUCTIVE['non'],
        REPRODUCTIVE['color'],
        REPRODUCTIVE['visible'],
        REPRODUCTIVE['and'],
        REPRODUCTIVE['uterus'],
        REPRODUCTIVE['tissue'],
        REPRODUCTIVE['present'],
        REPRODUCTIVE['active'],
        REPRODUCTIVE['developed'],
        REPRODUCTIVE['nipple'],

        keyword('false', """ false """),
        keyword('much', """ much """),

        keyword('lactation', r"""
            (indicate \s+)?
            (( previous | post | prior ) [\s-] )
            (lactation | lactating | lac )"""),

        keyword('other', """
            protuberant prominent showing worn distended
            """.split()),

        # Separates measurements
        fragment('separator', r' [;"?/,] '),

        # Skip arbitrary words
        fragment('word', r' \w+ '),
    ],

    replacers=[
        replacer('state_end', """
            ( size | fully | partially | other | lactation | color | false
                | visible | tissue | present | active | developed ) """),

        replacer('state_mid', """ ( uterus | and ) """),
    ],

    producers=[
        producer(
            convert,
            """(?P<value> non?
                (state_end | much) (state_mid | state_end){0,2} nipple)"""),

        producer(
            convert,
            """(?P<value> non? nipple
                (state_end | much) (state_mid | state_end){0,2} )"""),

        producer(
            convert,
            """(?P<value> nipple non?
                (state_end | much) (state_mid | state_end){0,2} )"""),
    ],
)
