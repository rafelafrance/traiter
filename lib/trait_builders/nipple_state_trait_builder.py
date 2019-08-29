"""Parse nipple state notations."""

from lib.trait_builders.base_trait_builder import BaseTraitBuilder
from lib.trait_builders.reproductive_trait_builder import FemaleTraitBuilder
from lib.shared_reproductive_patterns import ReproductivePatterns


class NippleStateTraitBuilder(BaseTraitBuilder, FemaleTraitBuilder):
    """Parser logic."""

    def build_token_rules(self):
        """Define the tokens."""
        r_tkn = ReproductivePatterns()

        self.copy(r_tkn['size'])
        self.copy(r_tkn['fully'])
        self.copy(r_tkn['partially'])
        self.copy(r_tkn['non'])
        self.copy(r_tkn['color'])
        self.copy(r_tkn['visible'])
        self.copy(r_tkn['and'])
        self.copy(r_tkn['uterus'])
        self.copy(r_tkn['tissue'])
        self.copy(r_tkn['present'])
        self.copy(r_tkn['active'])
        self.copy(r_tkn['developed'])
        self.copy(r_tkn['nipple'])

        self.keyword('false', """ false """)
        self.keyword('much', """ much """)

        self.keyword('lactation', r"""
            (indicate \s+)?
            (( previous | post | prior ) [\s-] )
            (lactation | lactating | lac )""")

        self.keyword('other', """
            protuberant prominent showing worn distended
            """.split())

        # Separates measurements
        self.fragment('separator', r' [;"?/,] ')

        # Skip arbitrary words
        self.fragment('word', r' \w+ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('state_end', """
            ( size | fully | partially | other | lactation | color | false
                | visible | tissue | present | active | developed ) """)
        self.replace('state_mid', """ ( uterus | and ) """)

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [
            """(?P<value> (non)?
                (state_end | much) (state_mid | state_end){0,2} nipple)""",

            """(?P<value> (non)? nipple
                (state_end | much) (state_mid | state_end){0,2} )""",

            """(?P<value> nipple (non)?
                (state_end | much) (state_mid | state_end){0,2} )""",
        ])
