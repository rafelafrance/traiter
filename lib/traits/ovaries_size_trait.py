"""Parse ovaries size notations."""

from operator import itemgetter
from lib.parse import Parse
from lib.traits.base_trait import BaseTrait, ordinal
import lib.shared_tokens as tkn
from lib.regexp import Regexp
from lib.token import Token


class OvariesSizeTrait(BaseTrait):
    """Parser logic."""

    side_pairs = {'left': 'right', 'right': 'left', '1': '2', '2': '1'}

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)
        self._build_token_rules()
        self._build_product_rules()

        self.finish_init()

    def _build_token_rules(self):
        self.shared_token(tkn.uuid)

    def _build_product_rules(self):
        pass
