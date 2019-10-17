"""Parse placental scar counts."""

from stacked_regex.rule import fragment, keyword, producer, replacer
from pylib.numeric_trait import NumericTrait
from pylib.parsers.base import Base
from pylib.shared_patterns import SHARED
from pylib.shared_reproductive_patterns import REPRODUCTIVE


def convert_count(token):
    """Convert parsed tokens into a result."""
    trait = NumericTrait(start=token.start, end=token.end)

    if token.groups.get('value'):
        trait.value = trait.to_int(token.groups['value'])
    elif token.groups.get('count1'):
        trait.value = trait.to_int(token.groups['count1'])
        trait.value += trait.to_int(token.groups.get('count2', ''))

    # Add scar side count
    side = token.groups.get('side1', '').lower()
    count = token.groups.get('count1', '').lower()
    if side:
        side = 'left' if side.startswith('l') else 'right'
        setattr(trait, side, trait.to_int(count))
    elif count:
        setattr(trait, 'side1', trait.to_int(count))

    # Add scar side count
    side = token.groups.get('side2', '').lower()
    count = token.groups.get('count2', '').lower()
    if side:
        side = 'left' if side.startswith('l') else 'right'
        setattr(trait, side, trait.to_int(count))
    elif count:
        setattr(trait, 'side2', trait.to_int(count))

    return trait


def convert_state(token):
    """Convert parsed tokens into a result."""
    trait = NumericTrait(value='present', start=token.start, end=token.end)
    return trait


PLACENTAL_SCAR_COUNT = Base(
    scanners=[
        SHARED['uuid'],  # UUIDs cause problems with numbers
        REPRODUCTIVE['plac_scar'],
        SHARED['integer'],
        REPRODUCTIVE['side'],
        REPRODUCTIVE['none'],
        REPRODUCTIVE['op'],
        REPRODUCTIVE['eq'],
        REPRODUCTIVE['embryo'],

        # Adjectives to placental scars
        keyword('adj', r"""
            faint prominent recent old possible """.split()),

        # Conjunction
        keyword('conj', ' or '.split()),

        # Preposition
        keyword('prep', ' on of '.split()),

        # Visible
        keyword('visible', ' visible definite '.split()),

        # Skip arbitrary words
        fragment('word', r' \w+ '),

        # Trait separator
        fragment('sep', r' [;/] '),
    ],

    replacers=[
        replacer('count', """
            none embryo conj
            | none visible | integer | none """),
    ],

    producers=[
        producer(convert_count, [
            """(?P<count1> count ) op (?P<count2> count )
                ( eq (?P<value> count ) )? plac_scar """]),

        producer(convert_count, [
            """plac_scar
                  (?P<count1> count ) (prep)? (?P<side1> side )
                ( (?P<count2> count ) (prep)? (?P<side2> side ) )? """]),

        producer(convert_count, [
            """ (?P<count1> count ) (prep)? (?P<side1> side ) plac_scar
                ( (?P<count2> count ) (prep)? (?P<side2> side )
                    (plac_scar)? )? """]),

        producer(convert_count, [
            """ (?P<side1> side ) (?P<count1> count )
                    (visible | op)? plac_scar
                ( (?P<side2> side ) (?P<count2> count )
                    (visible)? (visible | op)? (plac_scar)? )? """]),

        producer(convert_count, [
            """   (?P<count1> count ) (prep)? (?P<side1> side )
                ( (?P<count2> count ) (prep)? (?P<side2> side ) )?
                plac_scar """]),

        producer(convert_count, [
            """ (?P<count1> count ) plac_scar (?P<side1> side )
                ( (?P<count2> count ) plac_scar (?P<side2> side ) )? """]),

        producer(convert_count, [
            """ plac_scar (?P<side1> side ) (?P<count1> count )
                ( plac_scar (?P<side2> side ) (?P<count2> count ) )? """]),

        producer(convert_count, [
            """plac_scar
                (?P<count1> count )
                  op (?P<count2> count )
                ( eq (?P<value> count ) )? """]),

        producer(convert_count, [
            """ (?P<value> count ) (adj)? plac_scar (op)?
                (
                    (?P<count1> count ) (?P<side1> side )
                    (op)?
                    (?P<count2> count ) (?P<side2> side )
                )?
                """]),

        producer(convert_count, [
            """ (?P<value> count ) (embryo)? plac_scar """]),

        producer(convert_count, [
            """ plac_scar (eq)? (?P<count1> count ) (?P<side1> side ) """]),

        producer(convert_count, [
            """ plac_scar (eq)? (?P<value> count ) """]),

        producer(convert_state, """ plac_scar """),
    ],
)
