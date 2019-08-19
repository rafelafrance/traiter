"""Parse embryo lengths."""

from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
import lib.shared_tokens as tkn
import lib.shared_repoduction_tokens as r_tkn


class EmbryoLengthTraitBuilder(NumericTraitBuilder):
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
        self.shared_token(r_tkn.embryo)

        self.keyword('crown_rump', r""" 
            ( crown | cr ) ( [_\s\-] | \s+ to \s+ )? rump 
                | (?<! [a-z] ) crl (?! [a-z] ) 
                | (?<! [a-z] ) cr  (?! [a-z] ) """)

        self.keyword('length', r' length | len ')

        # Units
        self.shared_token(tkn.len_units)

        # Possible range of numbers like: "10 - 20" or just "10"
        self.shared_token(tkn.cross)

        # Separates measurements
        self.fragment('separator', r' [;"?/] ')

    def build_replace_rules(self):
        """Define rules for token simplification."""

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [

            # E.g.: crown-rump length=13 mm
            """ (embryo)? crown_rump (length)? 
                cross (?P<units> len_units )? """,

            # E.g.: 15 mm, crown-rump length
            """ (embryo)? cross (?P<units> len_units )? 
                crown_rump (length)? """,
        ])

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait product."""
        trait = NumericTrait(start=token.start, end=token.end)
        trait.cross_value(token)
        return trait

    def fix_problem_parses(self, trait, text):
        """Fix problematic parses."""
        # Try to disambiguate doubles quotes from inches
        return self.fix_up_inches(trait, text)

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        if not data['sex'] or data['sex'][0].value != 'male':
            return False
        if data[trait]:
            data[trait].skipped = "Skipped because sex is 'male'"
        return True
