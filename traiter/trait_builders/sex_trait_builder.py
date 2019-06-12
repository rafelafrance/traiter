"""Parse sex notations."""

import re
from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder


class SexTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        # The only keyword so far is: sex
        self.keyword('keyword', 'sex')

        # The sexes
        self.keyword('sex', 'females? males?'.split())

        # To handle a guessed sex
        self.fragment('quest', '[?]')

        # These are words that indicate that "sex" is not a key
        self.keyword('skip', 'and is was'.split())

        # Allow arbitrary words in some cases
        self.fragment('word', r' \b [a-z]\S* ')

        # Some patterns need a terminator
        self.fragment('sep', ' [;,"] | $ ')

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [

            # E.g.: sex might be female;
            'keyword (?P<value> ( sex | word ){1,2} ( quest )? ) sep',

            # E.g.: sex=female?
            # Or:   sex=unknown
            'keyword (?P<value> ( sex | word ) ( quest )? )',

            # E.g.: male
            # Or:   male?
            '(?P<value> sex ( quest )? )',
        ])

    def convert(self, token):
        """Convert parsed tokens into a result."""
        trait = Trait(
            value=token.groups['value'],
            start=token.start,
            end=token.end)
        trait.value = re.sub(r'\s*\?$', '?', trait.value, flags=self.flags)
        trait.value = re.sub(r'^m\w*', 'male', trait.value, flags=self.flags)
        trait.value = re.sub(r'^f\w*', 'female', trait.value, flags=self.flags)
        return trait
