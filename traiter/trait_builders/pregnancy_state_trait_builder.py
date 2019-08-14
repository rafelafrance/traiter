"""Parse sex notations."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder


class PregnancyStateTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        self.keyword('pregnant', r"""
            pregnant pregnan preg pregnancy pregnancies """.split())

        self.keyword('not', r""" not non no """.split())

        self.keyword('joiner', r""" of """.split())

        self.keyword('recent', r"""
            recently recent was previously prev """.split())

        self.keyword('probably', r"""
            probably prob possibly possible 
            appears? very
            visible visibly 
            evidence evident
            """.split())

        self.keyword('stage', r' early late mid '.split())

        self.fragment('quest', '[?]')

        self.fragment('separator', r' [;,"] ')

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [

            # E.g.: Probably early pregnancy
            """(?P<value> pregnant (not)? probably (quest)? )""",

            # E.g.: Probably early pregnancy
            """(?P<value> (not)? (recent | probably)?
                (stage)? (not | joiner)? pregnant (quest)? )""",
        ])

    @staticmethod
    def convert(token):
        """Convert parsed tokens into a result."""
        trait = Trait(
            value=token.groups['value'].lower(),
            start=token.start,
            end=token.end)
        return trait

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        if not data['sex'] or data['sex'][0].value != 'male':
            return False
        if data[trait]:
            data[trait].skipped = "Skipped because sex is 'male'"
        return True
