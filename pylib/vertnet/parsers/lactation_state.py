"""Parse lactation state notations."""

from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.parsers.base import Base, convert
import pylib.vertnet.shared_reproductive_patterns as patterns


CATALOG = RuleCatalog(patterns.CATALOG)


LACTATION_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        CATALOG.part('lactating', r""" (
            lactating | lactation | lactated | lactate | lact
            | lactaing | lactacting | lactataing | lactational
            | oelact | celact | lactati | lactacting | lactatin
            | lactatting | lactatng
            | nursing | suckling
            ) \b """),

        CATALOG.part('not', r' \b ( not | non | no ) '),

        CATALOG.part('post', r""" \b (
            (( just | recently ) \s+ )? finished
            | post | recently | recent | had | pre
            ) """),

        # Separates measurements
        CATALOG.part('separator', r' [;"/] '),
        CATALOG['word'],

        CATALOG.grouper('prefix', 'not post'.split()),

        CATALOG.producer(
            convert, """ (?P<value> prefix? lactating quest? ) """),
    ],
)
