"""Parse ovaries size notations."""

from traiter.traits.base_trait import BaseTrait
import traiter.shared_tokens as tkn


class OvariesSizeTrait(BaseTrait):
    """Parser logic."""

    side_pairs = {'left': 'right', 'right': 'left', '1': '2', '2': '1'}

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)
        self._build_token_rules()
        self._build_product_rules()

        self.compile_regex()

    def _build_token_rules(self):
        self.shared_token(tkn.uuid)

    def _build_product_rules(self):
        pass
