"""Parse embryo lengths."""

from pylib.shared.util import as_list, to_float
from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.trait import Trait
import pylib.shared.convert_units as convert_units
from pylib.vertnet.numeric import simple, add_flags, fix_up_inches
from pylib.vertnet.parsers.base import Base
import pylib.vertnet.shared_reproductive_patterns as patterns

CATALOG = RuleCatalog(patterns.CATALOG)


def convert(token):
    """Convert parsed token into a trait product."""
    trait = simple(token, units='len_units')
    return trait if all(x < 1000 for x in as_list(trait.value)) else None


def isolate(token):
    """Convert parsed token into a trait product."""
    token.groups['number'] = token.groups['real']
    return convert(token)


def convert_many(token):
    """Convert several values."""
    values = token.groups['value']
    units = as_list(token.groups.get('len_units', []))

    traits = []
    for i, value in enumerate(values):
        trait = Trait(start=token.start, end=token.end)
        if i < len(units):
            trait.units = units[i]
            trait.units_inferred = False
        else:
            trait.units = units[-1] if units else None
            trait.units_inferred = True
        trait.value = convert_units.convert(to_float(value), trait.units)
        add_flags(token, trait)
        traits.append(trait)
    return traits


def fix_up(trait, text):
    """Fix problematic parses."""
    # Try to disambiguate doubles quotes from inches
    return fix_up_inches(trait, text)


EMBRYO_LENGTH = Base(
    name=__name__.split('.')[-1],
    fix_up=fix_up,
    rules=[
        CATALOG.part('key', r"""
            (?<! collector [\s=:.] ) (?<! reg [\s=:.] ) (
                ( crown | cr ) ( [_\s\-] | \s+ to \s+ )? rump
                | (?<! [a-z] ) crl (?! [a-z] )
                | (?<! [a-z] ) cr  (?! [a-z] )
            )"""),

        CATALOG.part('other', r' \( \s* \d+ \s* \w+ \s* \) '),

        CATALOG.part('separator', r' [;"/.] '),

        CATALOG.grouper('noise', ' word x '.split()),
        CATALOG.grouper('value', ' cross | number len_units? '),

        CATALOG.grouper('count', """number side number side """),
        CATALOG.grouper('skip', ' prep word cross | other | side '),

        CATALOG.producer(convert_many, """
            embryo count? value{2,} (?! skip ) quest? """),
        CATALOG.producer(convert, """ embryo? key noise? value quest? """),
        CATALOG.producer(convert, """ embryo? noise? value key quest? """),
        CATALOG.producer(
            convert, """ embryo noise? value (?! skip ) quest? """),
        CATALOG.producer(isolate, """
            embryo count? (?P<real> value) len_units quest? """),
    ],
)
