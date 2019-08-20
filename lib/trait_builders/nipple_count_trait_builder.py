"""Parse lactation state notations."""

from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
import lib.shared_tokens as tkn
import lib.shared_repoduction_tokens as r_tkn


class NippleCountTraitBuilder(NumericTraitBuilder):
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
        self.shared_token(r_tkn.nipple)
        self.shared_token(tkn.integer)
        self.shared_token(r_tkn.visible)

        self.fragment('op', r' [+:] ')
        self.fragment('eq', r' [=] ')

        self.keyword('adj', r"""
            inguinal ing pectoral pec pr """.split())

        self.keyword('none', r""" no | none """)

        # Skip arbitrary words
        self.fragment('word', r' \w+ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('count', ' integer | none ')

        self.replace('modifier', 'adj visible'.split())

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.typed, [
            """ (?P<notation> 
                    (?P<value1> count) modifier
                    (?P<value2> count) modifier
                ) nipple """,
        ])

        self.product(self.convert, [

            # Eg: 1:2 = 6 mammae
            """ nipple (op)? 
                (?P<notation> count (modifier)? 
                    (op)? count (modifier)?
                    ((eq) (?P<value> count))? ) """,

            # Eg: 1:2 = 6 mammae
            """ (?P<notation> count (modifier)? (op)? count (modifier)?
                ((eq) (?P<value> count))? ) nipple """,

            # Eg: 6 mammae
            """ (?P<value> count ) (modifier)? nipple """,

            # Eg: nipples 5
            """ nipple (?P<value> count ) """,
        ])

    @staticmethod
    def convert(token):
        """Convert single value tokens into a result."""
        if not token.groups.get('value'):
            return None
        trait = NumericTrait(start=token.start, end=token.end)
        trait.value = trait.to_int(token.groups['value'])
        if token.groups.get('notation'):
            trait.notation = token.groups['notation']
        return trait

    @staticmethod
    def typed(token):
        """Convert single value tokens into a result."""
        trait = NumericTrait(start=token.start, end=token.end)
        trait.notation = token.groups['notation']
        trait.value = trait.to_int(token.groups['value1'])
        trait.value += trait.to_int(token.groups.get('value2'))
        return trait
