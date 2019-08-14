"""Parse hind foot length notations."""

from functools import partial
from traiter.trait_builders.numeric_trait_builder import NumericTraitBuilder
import traiter.shared_tokens as tkn


class HindFootLengthTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        # Units are in the key, like: HindFootLengthInMillimeters
        self.keyword(
            'key_with_units',
            r"""( hind \s* )? foot \s* ( length | len ) \s* in \s*
                    (?P<units> millimeters | mm )""")

        # Standard keywords that indicate a hind foot length follows
        self.keyword('key', [
            r'hind \s* foot \s* with \s* (?P<includes> claw )',
            r'hind \s* foot ( \s* ( length | len ) )?',
            'hfl | hf'])

        # Units
        self.shared_token(tkn.len_units)

        # Shorthand notation
        self.shared_token(tkn.shorthand_key)
        self.shared_token(tkn.shorthand)

        # Fractional numbers, like: 9/16
        self.shared_token(tkn.fraction)

        # Possible range of numbers like: "10 - 20" or just "10"
        self.shared_token(tkn.range_)

        # Sometimes the last number is missing in the shorthand notation
        self.shared_token(tkn.triple)

        # We allow random words in some situations
        self.keyword('word', r' ( [a-z] \w* ) ')

        # Some patterns require a separator
        self.fragment('sep', r' [;,] | $ ')

    def build_product_rules(self):
        """Define rules for output."""
        # Handle fractional values like: hindFoot 9/16"
        self.product(self.fraction, [

            # E.g.: hindFoot = 9/16 inches
            'key fraction (?P<units> len_units )',

            # E.g.: hindFoot = 9/16
            'key fraction'])

        # A typical body mass notation
        self.product(self.simple, [

            # E.g.: hindFootLengthInMM=9-10
            'key_with_units range',

            # E.g.: hindFootLength=9-10 mm
            'key range (?P<units> len_units )',

            # Missing units like: hindFootLength 9-10
            'key range'])

        self.product(partial(
            self.shorthand_length, measurement='shorthand_hfl'), [
                'shorthand_key shorthand',  # With a key
                'shorthand',                # Without a key
                # Handle a truncated shorthand notation
                'shorthand_key triple (?! shorthand | range )'])

    def fix_problem_parses(self, trait, text):
        """Fix problematic parses."""
        # Try to disambiguate doubles quotes from inches
        return self.fix_up_inches(trait, text)
