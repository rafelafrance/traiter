"""Parse nipple state notations."""

from lib.trait import Trait
from lib.trait_builders.base_trait_builder import BaseTraitBuilder
# import lib.shared_tokens as tkn
import lib.shared_repoduction_tokens as r_tkn


class NippleStateTraitBuilder(BaseTraitBuilder):
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
        self.shared_token(r_tkn.size)
        self.shared_token(r_tkn.fully)
        self.shared_token(r_tkn.partially)
        self.shared_token(r_tkn.non)
        self.shared_token(r_tkn.color)
        self.shared_token(r_tkn.visible)
        self.shared_token(r_tkn.and_)
        self.shared_token(r_tkn.uterus)
        self.shared_token(r_tkn.tissue)
        self.shared_token(r_tkn.present)
        self.shared_token(r_tkn.active)
        self.shared_token(r_tkn.developed)
        self.shared_token(r_tkn.nipple)

        self.keyword('false', """ false """)
        self.keyword('much', """ much """)

        self.keyword('lactation', r"""
            (indicate \s+)?
            (( previous | post | prior ) [\s-] )
            (lactation | lactating | lac )""")

        self.keyword('other', """
            protuberant prominent showing worn distended
            """.split())

        # Separates measurements
        self.fragment('separator', r' [;"?/] ')

        # Skip arbitrary words
        self.fragment('word', r' \w+ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('state_end', """
            ( size | fully | partially | other | lactation | color | false
                | visible | tissue | present | active | developed | and ) """)
        self.replace('state_mid', """ ( uterus | much ) """)

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [
            """(?P<value> (non)?
                (state_mid | state_end){0,2} state_end nipple)""",
            """(?P<value> (non)? nipple
                (state_mid | state_end){0,2} state_end)""",
            """(?P<value> nipple (non)?
                (state_mid | state_end){0,2} state_end)""",
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
