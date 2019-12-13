"""Parse lactation state notations."""

from pylib.stacked_regex.rule import frag, producer, grouper
from pylib.vertnet.parsers.base import Base, convert
from pylib.vertnet.shared_reproductive_patterns import RULE


LACTATION_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        frag('lactating', r""" (
            lactating | lactation | lactated | lactate | lact
            | lactaing | lactacting | lactataing | lactational
            | oelact | celact | lactati | lactacting | lactatin
            | lactatting | lactatng
            | nursing | suckling
            ) \b """),

        frag('not', r' \b ( not | non | no ) '),

        frag('post', r""" \b (
            (( just | recently ) \s+ )? finished
            | post | recently | recent | had | pre
            ) """),

        # To handle a guessed trait
        RULE['quest'],

        # Separates measurements
        frag('separator', r' [;"/] '),

        RULE['word'],

        grouper('prefix', 'not post'.split()),

        producer(convert, """ (?P<value> prefix? lactating quest? ) """),
    ],
)
