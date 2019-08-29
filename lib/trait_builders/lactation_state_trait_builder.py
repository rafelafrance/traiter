"""Parse lactation state notations."""

from lib.trait_builders.base_trait_builder import BaseTraitBuilder
from lib.trait_builders.reproductive_trait_builder import FemaleTraitBuilder
from lib.shared_reproductive_patterns import ReproductivePatterns


class LactationStateTraitBuilder(BaseTraitBuilder, FemaleTraitBuilder):
    """Parser logic."""

    def build_token_rules(self):
        """Define the tokens."""
        r_tkn = ReproductivePatterns()

        self.fragment('lactating', r""" (
            lactating | lactation | lactated | lactate | lact
            | lactaing | lactacting | lactataing | lactational
            | oelact | celact | lactati | lactacting | lactatin
            | lactatting | lactatng
            | nursing | suckling 
        ) \b """)

        self.fragment('not', r' \b ( not | non | no ) ')

        self.fragment('post', r""" \b (
            (( just | recently ) \s+ )? finished
            | post | recently | recent | had | pre
        ) """)

        # To handle a guessed trait
        self.fragment('quest', '[?]')

        # Separates measurements
        self.fragment('separator', r' [;"/] ')

        self.copy(r_tkn['word'])

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('prefix', 'not post'.split())

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [
            """ (?P<value> (prefix)? lactating (quest)? ) """
        ])
