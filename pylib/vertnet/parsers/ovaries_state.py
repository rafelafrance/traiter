"""Parse ovaries state notations."""

import regex
from pylib.stacked_regex.vocabulary import Vocabulary
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.base import Base
import pylib.vertnet.shared_reproductive_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)


def convert(token):
    """Convert parsed token into a trait."""
    value = token.group['value'].lower()
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
        value=token.group['value'][0].lower(),
        side=token.group['side'][0].lower(),
        start=token.start,
        end=token.end)

    trait2 = Trait(
        value=token.group['value'][1].lower(),
        side=token.group['side'][1].lower(),
        start=token.start,
        end=token.end)

    return [trait1, trait2]


OVARIES_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB.term('other', """ sev somewhat few """.split()),

        # Skip words
        VOCAB.term('skip', ' womb nullip '.split()),

        # VOCAB['comma'],
        VOCAB.part('sep', r' [;\(] '),

        # E.g.: ovaries and uterine horns
        # Or:   ovaries and fallopian tubes
        VOCAB.grouper('ovaries', r"""
            ovary ( ( and? uterus horns? ) | and? fallopian )?
            """),

        # E.g.: covered in copious fat
        VOCAB.grouper('coverage', ' covered word{0,2} fat '),

        # E.g.: +corpus luteum
        VOCAB.grouper('luteum', ' sign? corpus? (alb | lut) '),

        VOCAB.grouper('value_words', """
            size mature coverage luteum color corpus other active destroyed alb
            visible developed cyst texture fallopian luteum """.split()),

        VOCAB.grouper('values', """
            ( value_words ( and | comma ) | non )? 
            value_words """),

        VOCAB.producer(convert, """
            side? ovaries side? ( word | number | comma ){0,5} 
            (?P<value> values+ ) """),

        VOCAB.producer(convert, """
            (?P<value> values+ ) ( word | number | comma ){0,5}
               ( (?<! comma ) side )? (?<! comma ) ovaries """),

        # Get left and right side measurements
        # E.g.: ovaries: R 2 c. alb, L sev c. alb
        VOCAB.producer(double, r"""
            ovaries
                (?P<side> side) number? (?P<value> word? values+ )
                ( and | comma )?
                (?P<side> side) number? (?P<value> word? values+ )
            """),

    ],
)
