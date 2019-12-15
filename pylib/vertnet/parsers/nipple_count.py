"""Parse lactation state notations."""

from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.shared.util import to_int
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.trait import Trait
import pylib.vertnet.shared_reproductive_patterns as patterns


CATALOG = RuleCatalog(patterns.CATALOG)


def convert(token):
    """Convert single value tokens into a result."""
    value = token.groups.get('value')

    if not value:
        return None

    trait = Trait(start=token.start, end=token.end)
    trait.value = to_int(value)

    if trait.value > 100:
        return None

    if token.groups.get('notation'):
        trait.notation = token.groups['notation']

    return trait


def typed(token):
    """Convert single value tokens into a result."""
    trait = Trait(start=token.start, end=token.end)
    trait.notation = token.groups['notation']
    trait.value = to_int(token.groups['value1'])
    trait.value += to_int(token.groups.get('value2'))
    return trait


NIPPLE_COUNT = Base(
    name=__name__.split('.')[-1],
    rules=[
        # CATALOG['uuid'],  # UUIDs cause problems with numbers

        CATALOG.term('id', r' \d+-\d+ '),

        # CATALOG['nipple'],
        # CATALOG['integer'],
        # CATALOG['visible'],
        # CATALOG['none'],
        # CATALOG['op'],
        # CATALOG['eq'],

        CATALOG.term('adj', r""" inguinal ing pectoral pec pr """.split()),

        CATALOG.part('number', r' number | no | [#] '),
        CATALOG.part('eq', r' is | eq | equals? | [=] '),

        # Skip arbitrary words
        CATALOG['word'],
        CATALOG['sep'],

        CATALOG.grouper('count', ' integer | none '),

        CATALOG.grouper('modifier', 'adj visible'.split()),

        CATALOG.grouper('skip', ' number eq? integer '),

        CATALOG.producer(
            typed,
            """ (?P<notation>
                    (?P<value1> count) modifier
                    (?P<value2> count) modifier
                ) nipple """),

        # Eg: 1:2 = 6 mammae
        CATALOG.producer(
            convert,
            """ nipple op?
                (?P<notation> count modifier?
                    op? count modifier?
                    (eq (?P<value> count))? ) """),

        # Eg: 1:2 = 6 mammae
        CATALOG.producer(
            convert,
            """ (?P<notation> count modifier? op? count modifier?
                (eq (?P<value> count))? ) nipple """),

        # Eg: 6 mammae
        CATALOG.producer(convert, """ (?P<value> count ) modifier? nipple """),

        # Eg: nipples 5
        CATALOG.producer(convert, """ nipple (?P<value> count ) """),
    ],
)
