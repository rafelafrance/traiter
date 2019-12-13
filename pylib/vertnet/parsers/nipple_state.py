"""Parse nipple state notations."""

from pylib.stacked_regex.rule import part, term, producer, grouper
from pylib.vertnet.parsers.base import Base, convert
from pylib.vertnet.shared_reproductive_patterns import RULE


NIPPLE_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        RULE['size'],
        RULE['fully'],
        RULE['partially'],
        RULE['non'],
        RULE['color'],
        RULE['visible'],
        RULE['and'],
        RULE['uterus'],
        RULE['tissue'],
        RULE['present'],
        RULE['active'],
        RULE['developed'],
        RULE['nipple'],

        term('false', """ false """),
        term('much', """ much """),

        term('lactation', r"""
            (indicate \s+)?
            (( previous | post | prior ) [\s-] )
            (lactation | lactating | lac )"""),

        term('other', """
            protuberant prominent showing worn distended
            """.split()),

        # Separates measurements
        part('separator', r' [;"?/,] '),

        # Skip arbitrary words
        part('word', r' \w+ '),

        grouper('state_end', """
            ( size | fully | partially | other | lactation | color | false
                | visible | tissue | present | active | developed ) """),

        grouper('state_mid', """ ( uterus | and ) """),

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
