"""Parse body mass notations."""

from pylib.shared.util import as_list, squash
from pylib.stacked_regex.rule import fragment, keyword, producer, replacer
from pylib.vertnet.convert_units import convert
from pylib.vertnet.numeric_trait import NumericTrait
from pylib.vertnet.parsers.base import Base
from pylib.vertnet.parsers.numeric import simple
from pylib.vertnet.shared_patterns import RULE


def shorthand(token):
    """Convert a shorthand value like 11-22-33-44:55g."""
    # Handling shorthand notation for weights is different from lengths
    trait = NumericTrait(start=token.start, end=token.end)
    trait.float_value(token.groups.get('shorthand_wt'))
    if not trait.value:
        return None
    trait.convert_value(token.groups.get('shorthand_wt_units'))
    trait.is_flag_in_token('estimated_wt', token, rename='estimated_value')
    trait.is_shorthand = True
    return trait


def compound(token):
    """Convert a compound weight like: 2 lbs. 3.1 - 4.5 oz."""
    trait = NumericTrait(start=token.start, end=token.end)
    setattr(trait, 'units', [token.groups['pounds'], token.groups['ounces']])
    setattr(trait, 'units_inferred', False)
    trait.is_flag_missing('key', token, rename='ambiguous_key')
    lbs = convert(trait.to_float(token.groups['lbs']), 'lbs')
    ozs = [convert(trait.to_float(oz), 'ozs')
           for oz in as_list(token.groups['ozs'])]
    value = [round(lbs + oz, 2) for oz in ozs]
    setattr(trait, 'value', squash(value))
    return trait


BODY_MASS = Base(
    name=__name__.split('.')[-1],
    rules=[
        RULE['uuid'],  # UUIDs cause problems with numbers

        # Looking for keys like: MassInGrams
        keyword('key_with_units', r"""
        ( weight | mass) [\s-]* in [\s-]* (?P<units> grams | g | lbs ) """),

        # These words indicate a body mass follows
        fragment('key_leader', 'full observed total'.split()),

        # Words for weight
        fragment('weight', 'weights? weigh(ed|ing|s)?'.split()),

        # Keys like: w.t.
        fragment('key_with_dots', r' \b w \.? \s? t s? \.? '),

        # Common prefixes that indicate a body mass
        fragment('mass', 'mass'),
        fragment('body', 'body'),

        # Shorthand notation
        RULE['shorthand_key'],
        RULE['shorthand'],

        # Possible range of numbers like: 10 - 20
        # Or just: 10
        RULE['range_set'],

        # compound weight like 2 lbs. 3.1 - 4.5 oz
        RULE['compound_wt_set'],

        # These indicate that the mass is NOT a body mass
        keyword('other_wt', r"""
            femur baculum bacu bac spleen thymus kidney
            testes testis ovaries epididymis epid """.split()),

        # We allow random words in some situations
        keyword('word', r' ( [a-z] \w* ) '),

        # Separators
        RULE['semicolon'],
        RULE['comma'],

        # Any key not preceding by "other_wt" is considered a weight key
        replacer('wt_key', r"""
            (?<! other_wt )
            ( key_leader weight | key_leader mass
                | body weight | body mass | body
                | weight | mass | key_with_dots )
            """),

        replacer('key', ' shorthand_key wt_key '.split()),

        producer(compound, ' key? compound_wt '),

        # Shorthand notation like: on tag: 11-22-33-44=99g
        producer(shorthand, [
            'key shorthand',  # With a key
            'shorthand',     # Without a key
        ]),

        producer(simple, ' key units number (?! units ) '),
        producer(simple, ' key range '),
        producer(simple, ' (?P<key> key_with_units ) range '),
        ],
    )
