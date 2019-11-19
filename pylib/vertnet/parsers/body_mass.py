"""Parse body mass notations."""

from pylib.stacked_regex.rule import fragment, keyword, producer, replacer
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
    """"""
    units = token.groups.get('units')
    if len(units) != 2:
        return simple(token)
    print(token)
    return simple(token)


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

        # These indicate that the mass is NOT a body mass
        keyword('other_wt', r"""
        femur baculum bacu bac spleen thymus kidney
        testes testis ovaries epididymis epid """.split()),

        # We allow random words in some situations
        keyword('word', r' ( [a-z] \w* ) '),

        # Separators
        fragment('semicolon', ' [;] | $ '),
        fragment('comma', ' [,] | $ '),

        # Any key not preceding by "other_wt" is considered a weight key
        replacer('wt_key', r"""
            (?<! other_wt )
            ( key_leader weight | key_leader mass
                | body weight | body mass | body
                | weight | mass | key_with_dots )
            """),

        # Shorthand notation like: on tag: 11-22-33-44=99g
        producer(shorthand, [
            'shorthand_key shorthand',  # With a key
            'shorthand',  # Without a key
        ]),

        producer(compound, ' (?P<high> range ) (?P<low> range ) '),
        producer(simple, ' wt_key units number '),
        producer(simple, ' wt_key range '),

        # # E.g.: body mass: 5lbs, 3-4oz
        # producer(
        #     partial(compound, units=['lbs', 'ozs']),
        #     """wt_key (?P<lbs> range ) pounds comma?
        #         (?P<ozs> range ) ounces""",
        # ),
        #
        # # Missing a weight key: 5lbs, 3-4oz
        # producer(
        #     partial(compound, units=['lbs', 'ozs']),
        #     """(?P<ambiguous_key>
        #         (?P<lbs> range ) pounds comma?
        #         (?P<ozs> range ) ounces )""",
        # ),
        #
        # # A typical body mass notation
        # # E.g.: MassInGrams=22
        # producer(simple, 'key_with_units range'),
        #
        # # E.g.: body weight ozs 26 - 42
        # producer(
        #     simple,
        #     """wt_key (?P<units> metric_mass | pounds | ounces )
        #         range (?! len_units )"""),
        #
        # # E.g.: body weight 26 - 42 grams
        # producer(
        #     simple,'wt_key range (?P<units> metric_mass | pounds | ounces )'),
        #
        # # E.g.: measurement 26 - 42 grams
        # producer(
        #     simple,
        #     'shorthand_key range (?P<units> metric_mass | pounds | ounces )'),
        #
        # producer(
        #     simple,
        #     # E.g.: specimen: 8 to 15 grams"
        #     """shorthand_key (?P<units> metric_mass | pounds | ounces )
        #         range (?! len_units )"""),
        #
        # # E.g.: body mass 8 to 15 grams"
        # producer(simple, 'wt_key range (?! len_units )'),
    ],
)
