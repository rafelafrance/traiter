"""Parse ovaries size notations."""

from traiter.trait_builders.base_trait_builder import BaseTraitBuilder
import traiter.shared_tokens as tkn


class OvariesSizeTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    side_pairs = {'left': 'right', 'right': 'left', '1': '2', '2': '1'}

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)
        self.build_token_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        self.shared_token(tkn.uuid)

    def build_product_rules(self):
        """Define rules for output."""
