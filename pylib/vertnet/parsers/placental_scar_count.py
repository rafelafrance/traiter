"""Parse placental scar counts."""

from pylib.shared.util import as_list, to_int
from pylib.stacked_regex.vocabulary import Vocabulary
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.base import Base
import pylib.vertnet.shared_reproductive_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)

SUB = {'l': 'left', 'r': 'right', 'm': 'male', 'f': 'female'}


def convert_count(token):
    """Convert parsed tokens into a result."""
    trait = Trait(start=token.start, end=token.end)

    trait.value = to_int(token.group.get('value'))
    count1 = to_int(token.group.get('count1'))
    count2 = to_int(token.group.get('count2'))
    side1 = SUB.get(token.group.get('side1', ' ').lower()[0], 'side1')
    side2 = SUB.get(token.group.get('side2', ' ').lower()[0], 'side2')

    if not trait.value:
        trait.value = count1 + count2

    if count1 or side1 != 'side1':
        setattr(trait, side1, count1)

    if count2 or side2 != 'side2':
        setattr(trait, side2, count2)

    return trait if all(x < 1000 for x in as_list(trait.value)) else None


def convert_state(token):
    """Convert parsed tokens into a result."""
    trait = Trait(value='present', start=token.start, end=token.end)
    return trait


PLACENTAL_SCAR_COUNT = Base(
    name=__name__.split('.')[-1],
    rules=[
        # Adjectives to placental scars
        VOCAB.term('adj', r"""
            faint prominent recent old possible """.split()),

        # Skip arbitrary words
        VOCAB['word'],
        VOCAB.part('sep', r' [;/] '),

        VOCAB.grouper('count', """
            none embryo conj
            | none visible | integer | none """),

        VOCAB.producer(convert_count, [
            """(?P<count1> count ) op (?P<count2> count )
                ( eq (?P<value> count ) )? plac_scar """]),

        VOCAB.producer(convert_count, [
            """plac_scar
                  (?P<count1> count ) prep? (?P<side1> side )
                ( (?P<count2> count ) prep? (?P<side2> side ) )? """]),

        VOCAB.producer(convert_count, [
            """ (?P<count1> count ) prep? (?P<side1> side ) plac_scar
                ( (?P<count2> count ) prep? (?P<side2> side )
                    (plac_scar)? )? """]),

        VOCAB.producer(convert_count, [
            """ (?P<side1> side ) (?P<count1> count )
                    (visible | op)? plac_scar
                ( (?P<side2> side ) (?P<count2> count )
                    (visible)? (visible | op)? plac_scar? )? """]),

        VOCAB.producer(convert_count, [
            """   (?P<count1> count ) prep? (?P<side1> side )
                ( (?P<count2> count ) prep? (?P<side2> side ) )?
                plac_scar """]),

        VOCAB.producer(convert_count, [
            """ (?P<count1> count ) plac_scar (?P<side1> side )
                ( (?P<count2> count ) plac_scar (?P<side2> side ) )? """]),

        VOCAB.producer(convert_count, [
            """ plac_scar (?P<side1> side ) (?P<count1> count )
                ( plac_scar (?P<side2> side ) (?P<count2> count ) )? """]),

        VOCAB.producer(convert_count, [
            """plac_scar
                (?P<count1> count )
                  op (?P<count2> count )
                ( eq (?P<value> count ) )? """]),

        VOCAB.producer(convert_count, [
            """ (?P<value> count ) adj? plac_scar op?
                (
                    (?P<count1> count ) (?P<side1> side )
                    op?
                    (?P<count2> count ) (?P<side2> side )
                )?
                """]),

        VOCAB.producer(convert_count, [
            """ (?P<value> count ) embryo? plac_scar """]),

        VOCAB.producer(convert_count, [
            """ plac_scar eq? (?P<count1> count ) (?P<side1> side ) """]),

        VOCAB.producer(convert_count, [
            """ plac_scar eq? (?P<value> count ) """]),

        VOCAB.producer(convert_state, """ plac_scar """),
    ],
)
