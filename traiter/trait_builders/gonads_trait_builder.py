"""Holds rules common to both testes & ovaries size & state builders."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder
import traiter.shared_tokens as tkn
import traiter.writers.csv_formatters.testes_state_csv_formatter as \
    testes_state_csv_formatter


class GonadTraitBuilder(BaseTraitBuilder):
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

    def build_replace_rules(self):
        """Define rules for token simplification."""

    def build_product_rules(self):
        """Define rules for output."""
