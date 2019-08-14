"""Parse embryo counts."""

from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
import lib.shared_repoduction_tokens as r_tkn


class EmbryoCountTraitBuilder(NumericTraitBuilder):
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
        self.shared_token(r_tkn.embryo)

        self.fragment('integer', r""" \b \d+ """)
        self.keyword('none', r""" no | none """)

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('count', 'integer none'.split())

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [
            # Eg: 5 embryos
            """ (?P<value> count) embryo """
        ])

    @staticmethod
    def convert(token):
        """Convert parsed tokens into a result."""
        trait = NumericTrait(start=token.start, end=token.end)
        trait.value = trait.to_int(token.groups['value'])
        return trait

    @staticmethod
    def split(token):
        """Split a single token into multiple traits."""

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        if not data['sex'] or data['sex'][0].value != 'male':
            return False
        if data[trait]:
            data[trait].skipped = "Skipped because sex is 'male'"
        return True
