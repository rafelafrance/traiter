"""Parse pregnancy state notations."""

from lib.trait import Trait
from lib.trait_builders.base_trait_builder import BaseTraitBuilder
import lib.shared_repoduction_tokens as r_tkn


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
        self.shared_token(r_tkn.none)

        self.keyword('pregnant', r"""
            prega?n?ant pregnan preg pregnancy pregnancies 
            gravid multiparous nulliparous parous """.split())

        self.keyword('joiner', r""" of were """.split())

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

        # Skip arbitrary words
        self.fragment('word', r' [a-z]\w+ ')

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [

            # E.g.: pregnancy visible
            """(?P<value> pregnant (joiner)? (none)? probably (quest)? )""",

            # E.g.: Probably early pregnancy
            """(?P<value> (none)? (recent | probably)?
                (stage)? (none | joiner)? pregnant (quest)? )""",
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
