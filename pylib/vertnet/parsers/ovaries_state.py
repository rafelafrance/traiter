"""Parse ovaries state notations."""

import regex
from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.base import Base
import pylib.vertnet.shared_reproductive_patterns as patterns

CATALOG = RuleCatalog(patterns.CATALOG)


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
        CATALOG.term('other', """ sev somewhat few """.split()),

        # Skip words
        CATALOG.term('skip', ' womb nullip '.split()),

        # CATALOG['comma'],
        CATALOG.part('sep', r' [;\(] '),

        # E.g.: ovaries and uterine horns
        # Or:   ovaries and fallopian tubes
        CATALOG.grouper('ovaries', r"""
            ovary ( ( and? uterus horns? ) | and? fallopian )?
            """),

        # E.g.: covered in copious fat
        CATALOG.grouper('coverage', ' covered word{0,2} fat '),

        # E.g.: +corpus luteum
        CATALOG.grouper('luteum', ' sign? corpus? (alb | lut) '),

        CATALOG.grouper('value_words', """
            size mature coverage luteum color corpus other active destroyed alb
            visible developed cyst texture fallopian luteum """.split()),

        CATALOG.grouper('values', """
            ( value_words ( and | comma ) | non )? 
            value_words """),

        CATALOG.producer(convert, """
            side? ovaries side? ( word | number | comma ){0,5} 
            (?P<value> values+ ) """),

        CATALOG.producer(convert, """
            (?P<value> values+ ) ( word | number | comma ){0,5}
               ( (?<! comma ) side )? (?<! comma ) ovaries """),

        # Get left and right side measurements
        # E.g.: ovaries: R 2 c. alb, L sev c. alb
        CATALOG.producer(double, r"""
            ovaries
                (?P<side> side) number? (?P<value> word? values+ )
                ( and | comma )?
                (?P<side> side) number? (?P<value> word? values+ )
            """),

    ],
)
