"""Parse lactation state notations."""

from pylib.stacked_regex.rule import fragment, producer, replacer
from pylib.vertnet.parsers.base import Base, convert
from pylib.vertnet.shared_reproductive_patterns import RULE


LACTATION_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        fragment('lactating', r""" (
            lactating | lactation | lactated | lactate | lact
            | lactaing | lactacting | lactataing | lactational
            | oelact | celact | lactati | lactacting | lactatin
            | lactatting | lactatng
            | nursing | suckling
            ) \b """),

        fragment('not', r' \b ( not | non | no ) '),

        fragment('post', r""" \b (
            (( just | recently ) \s+ )? finished
            | post | recently | recent | had | pre
            ) """),

        # To handle a guessed trait
        RULE['quest'],

        # Separates measurements
        fragment('separator', r' [;"/] '),

        RULE['word'],

        replacer('prefix', 'not post'.split()),

        producer(convert, """ (?P<value> prefix? lactating quest? ) """),
    ],
)
