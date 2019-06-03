"""Just grab the notations as they are."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder


class AsIsTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.lit('data', r' \S .* \S | \S')

        # Build rules for parsing the trait
        self.product(self.convert, r' (?P<value> data )')

        self.compile_regex()

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait product."""
        return Trait(
            value=token.groups['value'],
            as_is=True,
            start=token.start,
            end=token.end)
