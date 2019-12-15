"""Parse body mass notations."""

from pylib.shared.util import as_list, squash, to_float
from pylib.shared.convert_units import convert
from pylib.stacked_regex.rule_catalog import RuleCatalog, LAST
from pylib.vertnet.trait import Trait
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.numeric import as_value, add_flags, simple_mass
import pylib.vertnet.shared_patterns as patterns


CATALOG = RuleCatalog(patterns.CATALOG)


def shorthand(token):
    """Convert a shorthand value like 11-22-33-44:55g."""
    trait = Trait(start=token.start, end=token.end)
    flag = as_value(token, trait, 'shorthand_wt', 'shorthand_wt_units')
    trait.is_flag_in_token(token, 'estimated_wt', rename='estimated_value')
    trait.is_shorthand = True
    return trait if flag else None


def compound(token):
    """Convert a compound weight like: 2 lbs. 3.1 - 4.5 oz."""
    trait = Trait(start=token.start, end=token.end)
    setattr(trait, 'units', [token.groups['pounds'], token.groups['ounces']])
    setattr(trait, 'units_inferred', False)
    trait.is_flag_missing(token, 'key', rename='ambiguous_key')
    lbs = convert(to_float(token.groups['lbs']), 'lbs')
    ozs = [convert(to_float(oz), 'ozs') for oz in as_list(token.groups['ozs'])]
    value = [round(lbs + oz, 2) for oz in ozs]
    setattr(trait, 'value', squash(value))
    add_flags(token, trait)
    return trait


BODY_MASS = Base(
    name=__name__.split('.')[-1],
    rules=[
        CATALOG['uuid'],  # UUIDs cause problems with numbers

        # Looking for keys like: MassInGrams
        CATALOG.term('key_with_units', r"""
            ( weight | mass) [\s-]* in [\s-]*
            (?P<mass_units> grams | g | lbs )"""),

        # These words indicate a body mass follows
        CATALOG.part('key_leader', 'full observed total'.split()),

        # Words for weight
        CATALOG.part('weight', 'weights? weigh(ed|ing|s)?'.split()),

        # Keys like: w.t.
        CATALOG.part('key_with_dots', r' \b w \.? \s? t s? \.? '),

        # Common prefixes that indicate a body mass
        CATALOG.part('mass', 'mass'),
        CATALOG.part('body', 'body'),


        # These indicate that the mass is NOT a body mass
        CATALOG.term('other_wt', r"""
            femur baculum bacu bac spleen thymus kidney
            testes testis ovaries epididymis epid """.split()),

        # Separators
        CATALOG['word'],
        CATALOG['semicolon'],
        CATALOG['comma'],

        # Any key not preceding by "other_wt" is considered a weight key
        CATALOG.grouper('wt_key', r"""
            (?<! other_wt )
            ( key_leader weight | key_leader mass
                | body weight | body mass | body
                | weight | mass | key_with_dots )
            """),

        CATALOG.grouper('key', ' shorthand_key wt_key '.split()),

        CATALOG.producer(compound, ' key? compound_wt '),

        # Shorthand notation like: on tag: 11-22-33-44=99g
        CATALOG.producer(shorthand, [
            'key shorthand',  # With a key
            'shorthand',     # Without a key
        ]),

        CATALOG.producer(
            simple_mass, ' key mass_units number (?! len_units ) '),
        CATALOG.producer(
            simple_mass, ' key mass_range '),
        CATALOG.producer(
            simple_mass, ' (?P<key> key_with_units ) mass_range '),
        ],
    )
