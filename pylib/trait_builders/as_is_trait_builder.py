"""Just grab the notations as they are."""

from pylib.trait import Trait
from pylib.trait_builders.base_trait_builder import BaseTraitBuilder


class AsIsTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    def build_token_rules(self):
        """Define the tokens."""
        self.fragment('data', [
            r' \S .* \S ',  # Strip leading and trailing spaces
            r' \S '])       # Get a string with a single character

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, '(?P<value> data )')

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait product."""
        return Trait(
            value=token.groups['value'],
            as_is=True,
            start=token.start, end=token.end)
