"""Parse lactation state notations."""

from pylib.stacked_regex.vocabulary import Vocabulary
from pylib.vertnet.parsers.base import Base, convert
import pylib.vertnet.shared_reproductive_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)

LACTATION_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB.part('lactating', r""" (
            lactating | lactation | lactated | lactate | lact
            | lactaing | lactacting | lactataing | lactational
            | oelact | celact | lactati | lactacting | lactatin
            | lactatting | lactatng
            | nursing | suckling
            ) \b """),

        VOCAB.part('not', r' \b ( not | non | no ) '),

        VOCAB.part('post', r""" \b (
            (( just | recently ) \s+ )? finished
            | post | recently | recent | had | pre
            ) """),

        # Separates measurements
        VOCAB.part('separator', r' [;"/] '),
        VOCAB['word'],

        VOCAB.grouper('prefix', 'not post'.split()),

        VOCAB.producer(
            convert, """ (?P<value> prefix? lactating quest? ) """),
    ],
)
