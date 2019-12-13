"""Parse ovaries state notations."""

import regex
from pylib.stacked_regex.rule import part, term, producer, grouper
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.shared_reproductive_patterns import RULE


def convert(token):
    """Convert parsed token into a trait."""
    value = token.groups['value'].lower()
    if regex.match(r'^[\s\d]+$', value):
        return None
    trait = Trait(
        value=value,
        start=token.start, end=token.end)
    trait.is_flag_in_token(token, 'ambiguous_key')
    trait.is_value_in_token(token, 'side')
    return trait


def double(token):
    """Convert a single token into two traits."""
    trait1 = Trait(
        value=token.groups['value'][0].lower(),
        side=token.groups['side'][0].lower(),
        start=token.start,
        end=token.end)

    trait2 = Trait(
        value=token.groups['value'][1].lower(),
        side=token.groups['side'][1].lower(),
        start=token.start,
        end=token.end)

    return [trait1, trait2]


OVARIES_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        RULE['ovary'],
        RULE['size'],
        RULE['mature'],
        RULE['corpus'],
        RULE['covered'],
        RULE['fat'],
        RULE['uterus'],
        RULE['fallopian'],
        RULE['active'],
        RULE['non'],
        RULE['visible'],
        RULE['destroyed'],
        RULE['developed'],
        RULE['horns'],
        RULE['lut'],
        RULE['alb'],
        RULE['nipple'],
        RULE['side'],
        RULE['cyst'],
        RULE['color'],
        RULE['texture'],
        RULE['sign'],
        RULE['and'],
        RULE['number'],
        RULE['embryo'],

        term('other', """ sev somewhat few """.split()),

        # Skip words
        term('skip', ' womb nullip '.split()),

        part('comma', r' [,] '),
        part('sep', r' [;\(] '),

        # We allow random words in some situations
        part('word', r'[a-z] \w*'),

        # E.g.: ovaries and uterine horns
        # Or:   ovaries and fallopian tubes
        grouper('ovaries', r"""
            ovary ( ( and? uterus horns? ) | and? fallopian )?
            """),

        # E.g.: covered in copious fat
        grouper('coverage', ' covered word{0,2} fat '),

        # E.g.: +corpus luteum
        grouper('luteum', ' sign? corpus? (alb | lut) '),

        grouper('value_words', """
            size mature coverage luteum color corpus other active destroyed alb
            visible developed cyst texture fallopian luteum """.split()),

        grouper('values', """
            ( value_words ( and | comma ) | non )? 
            value_words """),

        producer(convert, """
            side? ovaries side? ( word | number | comma ){0,5} 
            (?P<value> values+ ) """),

        producer(convert, """
            (?P<value> values+ ) ( word | number | comma ){0,5}
               ( (?<! comma ) side )? (?<! comma ) ovaries """),

        # Get left and right side measurements
        # E.g.: ovaries: R 2 c. alb, L sev c. alb
        producer(double, r"""
            ovaries
                (?P<side> side) number? (?P<value> word? values+ )
                ( and | comma )?
                (?P<side> side) number? (?P<value> word? values+ )
            """),

        ],
    )
