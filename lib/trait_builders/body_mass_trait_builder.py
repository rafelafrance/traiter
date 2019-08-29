"""Parse body mass notations."""

from functools import partial
from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from lib.shared_patterns import SharedPatterns


class BodyMassTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    def build_token_rules(self):
        """Define the tokens."""
        tkn = SharedPatterns()
        self.copy(tkn['uuid'])  # UUIDs cause problems with numbers

        # Looking for keys like: MassInGrams
        self.keyword('key_with_units', r"""
            ( weight | mass) [\s-]* in [\s-]* (?P<units> grams | g | lbs ) """)

        # These words indicate a body mass follows
        self.fragment('key_leader', 'full observed total'.split())

        # Words for weight
        self.fragment('weight', 'weights? weighed weighing weighs?'.split())

        # Keys like: w.t.
        self.fragment('key_with_dots', r' \b w \.? \s? t s? \.? ')

        # Common prefixes that indicate a body mass
        self.fragment('mass', 'mass')
        self.fragment('body', 'body')

        # Units
        self.copy(tkn['len_units'])
        self.copy(tkn['metric_mass'])
        self.copy(tkn['pounds'])
        self.copy(tkn['ounces'])

        # Shorthand notation
        self.copy(tkn['shorthand_key'])
        self.copy(tkn['shorthand'])

        # Possible range of numbers like: 10 - 20
        # Or just: 10
        self.copy(tkn['range'])

        # These indicate that the mass is NOT a body mass
        self.keyword('other_wt', r"""
            femur baculum bacu bac spleen thymus kidney
            testes testis ovaries epididymis epid """.split())

        # We allow random words in some situations
        self.keyword('word', r' ( [a-z] \w* ) ')

        # Separators
        self.fragment('semicolon', ' [;] | $ ')
        self.fragment('comma', ' [,] | $ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        # Any key not preceding by "other_wt" is considered a weight key
        self.replace('wt_key', r"""
            (?<! other_wt )
            ( key_leader weight | key_leader mass
                | body weight | body mass | body
                | weight | mass | key_with_dots )
            """)

    def build_product_rules(self):
        """Define rules for output."""
        # Shorthand notation like: on tag: 11-22-33-44=99g
        self.product(self.shorthand, [
            'shorthand_key shorthand',  # With a key
            'shorthand',                # Without a key
        ])

        # Pounds and ounces notation: 5lbs, 3-4oz.
        self.product(partial(self.compound, units=['lbs', 'ozs']), [

            # E.g.: body mass: 5lbs, 3-4oz
            'wt_key (?P<lbs> range ) pounds ( comma )? (?P<ozs> range ) ounces',

            # Missing a weight key: 5lbs, 3-4oz
            """(?P<ambiguous_key>
                (?P<lbs> range ) pounds ( comma )?
                (?P<ozs> range ) ounces )""",
        ])

        # A typical body mass notation
        self.product(self.simple, [

            # E.g.: MassInGrams=22
            'key_with_units range',

            # E.g.: body weight ozs 26 - 42
            """wt_key (?P<units> metric_mass | pounds | ounces )
                range (?! len_units )""",

            # E.g.: body weight 26 - 42 grams
            'wt_key range (?P<units> metric_mass | pounds | ounces )',

            # E.g.: measurement 26 - 42 grams
            'shorthand_key range (?P<units> metric_mass | pounds | ounces )',

            # E.g.: specimen: 8 to 15 grams"
            """shorthand_key (?P<units> metric_mass | pounds | ounces )
                range (?! len_units )""",

            # E.g.: body mass 8 to 15 grams"
            'wt_key range (?! len_units )',
        ])

    @staticmethod
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
