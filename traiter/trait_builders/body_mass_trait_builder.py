"""Parse body mass notations."""

from functools import partial
from traiter.numeric_trait import NumericTrait
from traiter.trait_builders.numeric_trait_builder import NumericTraitBuilder
import traiter.shared_tokens as tkn


class BodyMassTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_replace_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        self.shared_token(tkn.uuid)  # UUIDs cause problems with numeric parses

        # Looking for keys like: mass in grams
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
        self.shared_token(tkn.len_units)
        self.shared_token(tkn.metric_mass)
        self.shared_token(tkn.pounds)
        self.shared_token(tkn.ounces)

        # Shorthand notation
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)

        # Possible pairs of numbers like: "10 - 20" or just "10"
        self.shared_token(tkn.pair)

        # These indicate that the mass is NOT a total body mass
        self.keyword('other_wt', r"""
            femur baculum bacu bac spleen thymus kidney
            testes testis ovaries epididymis epid """.split())

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

            # Like: body mass: 5lbs, 3-4oz
            'wt_key (?P<lbs> pair ) pounds ( comma )? (?P<ozs> pair ) ounces',

            # Missing a weight key: 5lbs, 3-4oz
            """(?P<ambiguous_key>
                (?P<lbs> pair ) pounds ( comma )?
                (?P<ozs> pair ) ounces )""",
        ])

        # A typical body mass notation
        self.product(self.simple, [

            # Like: mass in grams: 22
            'key_with_units pair',

            # Like: body weight ozs 26 - 42
            """wt_key (?P<units> metric_mass | pounds | ounces )
                pair (?! len_units )""",

            # Like: body weight 26 - 42 grams
            'wt_key pair (?P<units> metric_mass | pounds | ounces )',

            # Like: body weight 26 - 42 grams
            'shorthand_key pair (?P<units> metric_mass | pounds | ounces )',

            # Like: specimen: 8 to 15 grams"
            """shorthand_key (?P<units> metric_mass | pounds | ounces )
                pair (?! len_units )""",

            # Like: body mass 8 to 15 grams"
            'wt_key pair (?! len_units )',
        ])

    @staticmethod
    def shorthand(token):
        """Convert a shorthand value like 11-22-33-44:55g."""
        trait = NumericTrait(start=token.start, end=token.end)
        trait.float_value(token.groups.get('shorthand_wt'))
        if not trait.value:
            return None
        trait.convert_value(token.groups.get('shorthand_wt_units'))
        trait.is_flag_in_token('estimated_wt', token, rename='estimated_value')
        trait.is_shorthand = True
        return trait