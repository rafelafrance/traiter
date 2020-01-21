"""Parse nipple state notations."""

from traiter.vocabulary import Vocabulary
from traiter_vertnet.parsers.base import Base, convert
import traiter_vertnet.shared_reproductive_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)

NIPPLE_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB.term('false', """ false """),
        VOCAB.term('much', """ much """),

        VOCAB.term('lactation', r"""
            (indicate \s+)?
            (( previous | post | prior ) [\s-] )
            (lactation | lactating | lac )"""),

        VOCAB.term('other', """
            protuberant prominent showing worn distended
            """.split()),

        # Separates measurements
        VOCAB.part('separator', r' [;"?/,] '),

        # Skip arbitrary words
        VOCAB['word'],

        VOCAB.grouper('state_end', """
            ( size | fully | partially | other | lactation | color | false
                | visible | tissue | present | active | developed ) """),

        VOCAB.grouper('state_mid', """ ( uterus | and ) """),

        VOCAB.producer(
            convert,
            """(?P<value> non?
                (state_end | much) (state_mid | state_end){0,2} nipple)"""),

        VOCAB.producer(
            convert,
            """(?P<value> non? nipple
                (state_end | much) (state_mid | state_end){0,2} )"""),

        VOCAB.producer(
            convert,
            """(?P<value> nipple non?
                (state_end | much) (state_mid | state_end){0,2} )"""),
    ],
)
