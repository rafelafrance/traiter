"""Parse lactation state notations."""

from pylib.stacked_regex.vocabulary import Vocabulary
from pylib.shared.util import to_int
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.trait import Trait
import pylib.vertnet.shared_reproductive_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)


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
        VOCAB.term('id', r' \d+-\d+ '),

        VOCAB.term('adj', r""" inguinal ing pectoral pec pr """.split()),

        VOCAB.part('number', r' number | no | [#] '),
        VOCAB.part('eq', r' is | eq | equals? | [=] '),

        # Skip arbitrary words
        VOCAB['word'],
        VOCAB['sep'],

        VOCAB.grouper('count', ' integer | none '),

        VOCAB.grouper('modifier', 'adj visible'.split()),

        VOCAB.grouper('skip', ' number eq? integer '),

        VOCAB.producer(
            typed,
            """ (?P<notation>
                    (?P<value1> count) modifier
                    (?P<value2> count) modifier
                ) nipple """),

        # Eg: 1:2 = 6 mammae
        VOCAB.producer(
            convert,
            """ nipple op?
                (?P<notation> count modifier?
                    op? count modifier?
                    (eq (?P<value> count))? ) """),

        # Eg: 1:2 = 6 mammae
        VOCAB.producer(
            convert,
            """ (?P<notation> count modifier? op? count modifier?
                (eq (?P<value> count))? ) nipple """),

        # Eg: 6 mammae
        VOCAB.producer(convert, """ (?P<value> count ) modifier? nipple """),

        # Eg: nipples 5
        VOCAB.producer(convert, """ nipple (?P<value> count ) """),
    ],
)
