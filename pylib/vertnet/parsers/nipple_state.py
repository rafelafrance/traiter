"""Parse nipple state notations."""

from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.parsers.base import Base, convert
import pylib.vertnet.shared_reproductive_patterns as patterns


CATALOG = RuleCatalog(patterns.CATALOG)


NIPPLE_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        CATALOG.term('false', """ false """),
        CATALOG.term('much', """ much """),

        CATALOG.term('lactation', r"""
            (indicate \s+)?
            (( previous | post | prior ) [\s-] )
            (lactation | lactating | lac )"""),

        CATALOG.term('other', """
            protuberant prominent showing worn distended
            """.split()),

        # Separates measurements
        CATALOG.part('separator', r' [;"?/,] '),

        # Skip arbitrary words
        CATALOG['word'],

        CATALOG.grouper('state_end', """
            ( size | fully | partially | other | lactation | color | false
                | visible | tissue | present | active | developed ) """),

        CATALOG.grouper('state_mid', """ ( uterus | and ) """),

        CATALOG.producer(
            convert,
            """(?P<value> non?
                (state_end | much) (state_mid | state_end){0,2} nipple)"""),

        CATALOG.producer(
            convert,
            """(?P<value> non? nipple
                (state_end | much) (state_mid | state_end){0,2} )"""),

        CATALOG.producer(
            convert,
            """(?P<value> nipple non?
                (state_end | much) (state_mid | state_end){0,2} )"""),
    ],
)
