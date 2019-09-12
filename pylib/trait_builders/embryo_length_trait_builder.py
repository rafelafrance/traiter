"""Parse embryo lengths."""

from pylib.numeric_trait import NumericTrait
from pylib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from pylib.trait_builders.reproductive_trait_builder import FemaleTraitBuilder
from pylib.shared_patterns import SharedPatterns
from pylib.shared_reproductive_patterns import ReproductivePatterns


class EmbryoLengthTraitBuilder(NumericTraitBuilder, FemaleTraitBuilder):
    """Parser logic."""

    def build_token_rules(self):
        """Define the tokens."""
        tkn = SharedPatterns()
        r_tkn = ReproductivePatterns()

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
