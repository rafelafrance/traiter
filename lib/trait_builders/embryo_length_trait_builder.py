"""Parse embryo lengths."""

from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from lib.shared_tokens import SharedTokens
from lib.shared_repoduction_tokens import ReproductiveTokens


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
        tkn = SharedTokens()
        r_tkn = ReproductiveTokens()

        self.copy(tkn['uuid'])  # UUIDs cause problems with numbers

        self.copy(r_tkn['embryo'])

        self.keyword('crown_rump', r"""
            (?<! collector [\s=:.] ) (?<! reg [\s=:.] ) (
                ( crown | cr ) ( [_\s\-] | \s+ to \s+ )? rump
                | (?<! [a-z] ) crl (?! [a-z] )
                | (?<! [a-z] ) cr  (?! [a-z] )
            )""")

        self.keyword('length', r' length | len ')

        self.keyword('prep', ' of from '.split())
        self.keyword('side', r""" left | right | lf | lt | rt | [lr] """)

        self.copy(tkn['len_units'])

        self.copy(tkn['cross'])
        self.fragment('cross_joiner', tkn['cross_joiner'].pattern)

        self.fragment('word', r' \w+ ')
        self.fragment('separator', r' [;"?/] ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('skip', ' prep word cross ')
        self.replace('measurement', ' (cross_joiner)? cross ')

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [

            # E.g.: crown-rump length=13 mm
            """ (embryo)? crown_rump (length)?
                measurement (?P<units> len_units )? """,

            # E.g.: 15 mm, crown-rump length
            """ (embryo)? measurement (?P<units> len_units )?
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
