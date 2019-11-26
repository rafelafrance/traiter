"""Parse embryo lengths."""

from pylib.stacked_regex.rule import fragment, producer, grouper
from pylib.shared.util import as_list, to_float
from pylib.vertnet.trait import Trait
import pylib.vertnet.convert_units as convert_units
from pylib.vertnet.parsers.numeric import simple, add_flags
from pylib.vertnet.parsers.numeric import fix_up_inches
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.shared_reproductive_patterns import RULE


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
        RULE['uuid'],  # UUIDs cause problems with numbers

        RULE['embryo'],

        fragment('key', r"""
            (?<! collector [\s=:.] ) (?<! reg [\s=:.] ) (
                ( crown | cr ) ( [_\s\-] | \s+ to \s+ )? rump
                | (?<! [a-z] ) crl (?! [a-z] )
                | (?<! [a-z] ) cr  (?! [a-z] )
            )"""),

        # keyword('length', r' length | len '),

        RULE['cross_set'],

        fragment('other', r' \( \s* \d+ \s* \w+ \s* \) '),

        RULE['side'],
        RULE['prep'],
        RULE['word'],
        RULE['quest'],
        fragment('separator', r' [;"/.] '),

        grouper('noise', ' word x '.split()),
        grouper('value', ' cross | number len_units? '),

        grouper('count', """number side number side """),
        grouper('skip', ' prep word cross | other | side '),
        # grouper('measurement', ' ( x | by )? cross '),

        producer(convert_many, """
            embryo count? value{2,} (?! skip ) quest? """),
        producer(convert, """ embryo? key noise? value quest? """),
        producer(convert, """ embryo? noise? value key quest? """),
        producer(convert, """ embryo noise? value (?! skip ) quest? """),
        producer(isolate, """
            embryo count? (?P<real> value) len_units quest? """),

        # producer(convert, [
        #     # E.g.: 15 mm, crown-rump length
        #     """ embryo? measurement quest? (?P<units> len_units )?
        #         crown_rump length? """,
        # ]),
        # producer(convert_many, [
        #     # E.g.: 15 mm, crown-rump length
        #     """ embryo count measurement{2,} (?! skip ) quest? """,
        # ]),
        #
        # producer(convert, [
        #     # E.g.: 15 mm, crown-rump length
        #     """ embryo count measurement (?! skip ) quest? """,
        # ]),
        #
        # producer(convert, [
        #     # E.g.: 15 mm, crown-rump length
        #     """ embryo word{0,3} measurement (?! skip ) quest? """,
        # ]),

    ],
)
