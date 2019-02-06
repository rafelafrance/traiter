"""Just grab the notations as they are."""

from lib.trait import Trait
from lib.traits.base_trait import BaseTrait


class AsIsTrait(BaseTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.lit('data', r' \S .* \S | \S')

        # Build rules for parsing the trait
        self.product(self.convert, r' (?P<value> data )')

        self.finish_init()

    def convert(self, token):  # pylint: disable=no-self-use
        """Convert parsed token into a trait product."""
        return Trait(
            value=token.groups['value'],
            as_is=True,
            start=token.start,
            end=token.end)
