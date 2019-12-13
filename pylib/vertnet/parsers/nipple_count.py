"""Parse lactation state notations."""

from pylib.stacked_regex.rule import frag, vocab, producer, grouper
from pylib.shared.util import to_int
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.trait import Trait
from pylib.vertnet.shared_reproductive_patterns import RULE


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
        RULE['uuid'],  # UUIDs cause problems with numbers

        vocab('id', r' \d+-\d+ '),

        RULE['nipple'],
        RULE['integer'],
        RULE['visible'],
        RULE['none'],
        RULE['op'],
        RULE['eq'],

        vocab('adj', r""" inguinal ing pectoral pec pr """.split()),

        frag('number', r' number | no | [#] '),
        frag('eq', r' is | eq | equals? | [=] '),

        # Skip arbitrary words
        frag('word', r' \w+ '),

        RULE['sep'],

        grouper('count', ' integer | none '),

        grouper('modifier', 'adj visible'.split()),

        grouper('skip', ' number eq? integer '),

        producer(
            typed,
            """ (?P<notation>
                    (?P<value1> count) modifier
                    (?P<value2> count) modifier
                ) nipple """),

        # Eg: 1:2 = 6 mammae
        producer(
            convert,
            """ nipple op?
                (?P<notation> count modifier?
                    op? count modifier?
                    (eq (?P<value> count))? ) """),

        # Eg: 1:2 = 6 mammae
        producer(
            convert,
            """ (?P<notation> count modifier? op? count modifier?
                (eq (?P<value> count))? ) nipple """),

        # Eg: 6 mammae
        producer(convert, """ (?P<value> count ) modifier? nipple """),

        # Eg: nipples 5
        producer(convert, """ nipple (?P<value> count ) """),
    ],
)
