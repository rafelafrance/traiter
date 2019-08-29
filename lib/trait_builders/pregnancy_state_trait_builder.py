"""Parse pregnancy state notations."""

from lib.trait_builders.base_trait_builder import BaseTraitBuilder
from lib.trait_builders.reproductive_trait_builder import FemaleTraitBuilder
from lib.shared_reproductive_patterns import ReproductivePatterns


class PregnancyStateTraitBuilder(BaseTraitBuilder, FemaleTraitBuilder):
    """Parser logic."""

    def build_token_rules(self):
        """Define the tokens."""
        r_tkn = ReproductivePatterns()

        self.copy(r_tkn['none'])

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
