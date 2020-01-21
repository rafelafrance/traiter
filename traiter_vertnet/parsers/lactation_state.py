"""Parse lactation state notations."""

from traiter.vocabulary import Vocabulary
from traiter_vertnet.parsers.base import Base, convert
import traiter_vertnet.shared_reproductive_patterns as patterns

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
