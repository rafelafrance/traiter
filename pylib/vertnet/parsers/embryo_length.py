"""Parse embryo lengths."""

from pylib.stacked_regex.rule import fragment, keyword, producer, grouper
from pylib.stacked_regex.token import forget
from pylib.vertnet.numeric_trait import NumericTrait
from pylib.vertnet.parsers.numeric import fix_up_inches
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.shared_reproductive_patterns import RULE


def convert(token):
    """Convert parsed token into a trait product."""
    trait = NumericTrait(start=token.start, end=token.end)
    trait.cross_value(token)
    trait.is_value_in_token('quest', token, rename='uncertain')
    return trait


def convert_many(token):
    """Only allow numeric values with units."""
    values = NumericTrait.all_values(
        token, ['value1', 'value2a', 'value2b', 'value2c'])
    units = NumericTrait.all_values(
        token, ['units', 'units1a', 'units1b', 'units1c', 'units2'])

    trim = min(len(values), len(units))
    values = values[:trim]
    units = units[:trim]

    traits = []
    for value, unit in zip(values, units):
        trait = NumericTrait(start=token.start, end=token.end)
        trait.float_value(value)
        trait.convert_value(unit)
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

        keyword('crown_rump', r"""
            (?<! collector [\s=:.] ) (?<! reg [\s=:.] ) (
                ( crown | cr ) ( [_\s\-] | \s+ to \s+ )? rump
                | (?<! [a-z] ) crl (?! [a-z] )
                | (?<! [a-z] ) cr  (?! [a-z] )
            )"""),

        keyword('length', r' length | len '),

        keyword('prep', ' of from '.split()),

        RULE['len_units'],

        RULE['cross'],
        fragment('cross_joiner', RULE['cross_joiner'].pattern),
        fragment('other', r' \( \s* \d+ \s* \w+ \s* \) '),

        keyword('count_side', r' \d+ \s? ( l[ft]? | rt? ) '),
        RULE['side'],
        fragment('word', r' \w+ '),
        fragment('quest', '[?]'),
        fragment('separator', r' [;"/] '),

        grouper(
            'count',
            """measurement side measurement side | count_side count_side """,
            action=forget),
        grouper('skip', ' prep word cross | other '),
        grouper('measurement', ' cross_joiner? cross '),

        producer(convert, [
            # E.g.: crown-rump length=13 mm
            """ embryo? crown_rump length?
                measurement (?P<units> len_units )? quest? """,
        ]),

        producer(convert, [
            # E.g.: 15 mm, crown-rump length
            """ embryo? measurement quest? (?P<units> len_units )?
                crown_rump length? """,
        ]),
        producer(convert_many, [
            # E.g.: 15 mm, crown-rump length
            """ embryo count measurement{2,} (?! skip ) quest? """,
        ]),

        producer(convert, [
            # E.g.: 15 mm, crown-rump length
            """ embryo count measurement (?! skip ) quest? """,
        ]),

        producer(convert, [
            # E.g.: 15 mm, crown-rump length
            """ embryo word{0,3} measurement (?! skip ) quest? """,
        ]),

    ],
)
