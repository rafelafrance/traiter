"""Parse lactation state notations."""

from stacked_regex.rule import fragment, keyword, producer, replacer
from pylib.parsers.base import Base
from pylib.numeric_trait import NumericTrait
from pylib.shared_patterns import SHARED
from pylib.shared_reproductive_patterns import REPRODUCTIVE


def convert(token):
    """Convert single value tokens into a result."""
    value = token.groups.get('value')

    if not value:
        return None

    trait = NumericTrait(start=token.start, end=token.end)
    trait.value = trait.to_int(value)

    if trait.value > 100:
        return None

    if token.groups.get('notation'):
        trait.notation = token.groups['notation']

    return trait


def typed(token):
    """Convert single value tokens into a result."""
    trait = NumericTrait(start=token.start, end=token.end)
    trait.notation = token.groups['notation']
    trait.value = trait.to_int(token.groups['value1'])
    trait.value += trait.to_int(token.groups.get('value2'))
    return trait


NIPPLE_COUNT = Base(
    scanners=[
        SHARED['uuid'],  # UUIDs cause problems with numbers

        keyword('id', r' \d+-\d+ '),

        REPRODUCTIVE['nipple'],
        SHARED['integer'],
        REPRODUCTIVE['visible'],
        REPRODUCTIVE['none'],
        REPRODUCTIVE['op'],
        REPRODUCTIVE['eq'],

        keyword('adj', r""" inguinal ing pectoral pec pr """.split()),

        fragment('number', r' number | no | [#] '),
        fragment('eq', r' is | eq | equals? | [=] '),

        # Skip arbitrary words
        fragment('word', r' \w+ '),

        REPRODUCTIVE['sep'],
    ],

    replacers=[
        replacer('count', ' integer | none '),

        replacer('modifier', 'adj visible'.split()),

        replacer('skip', ' number (eq)? integer '),
    ],

    producers=[
        producer(
            typed,
            """ (?P<notation>
                    (?P<value1> count) modifier
                    (?P<value2> count) modifier
                ) nipple """),

        # Eg: 1:2 = 6 mammae
        producer(
            convert,
            """ nipple (op)?
                (?P<notation> count (modifier)?
                    (op)? count (modifier)?
                    ((eq) (?P<value> count))? ) """),

        # Eg: 1:2 = 6 mammae
        producer(
            convert,
            """ (?P<notation> count (modifier)? (op)? count (modifier)?
                ((eq) (?P<value> count))? ) nipple """),

        # Eg: 6 mammae
        producer(convert, """ (?P<value> count ) (modifier)? nipple """),

        # Eg: nipples 5
        producer(convert, """ nipple (?P<value> count ) """),
    ],
)
