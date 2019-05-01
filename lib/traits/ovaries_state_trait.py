"""Parse testes state notations."""

from lib.parse import Parse
from lib.traits.base_trait import BaseTrait, ordinal
import lib.shared_tokens as tkn


class OvariesStateTrait(BaseTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)
