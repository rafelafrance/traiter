"""Parse sex notations."""

import re
from traiter.parse import Parse
from traiter.traits.base_trait import BaseTrait


class SexTrait(BaseTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self._build_token_rules()
        self._build_product_rules()

        self.compile_regex()

    def _build_token_rules(self):
        self.kwd('keyword', 'sex')
        self.kwd('sex', r' females? | males? ')
        self.lit('quest', r' \? ')

        # These are words that indicate that "sex" is not a key
        self.kwd('skip', r' and | is | was ')
        self.lit('word', r' \b [a-z]\S* ')
        self.lit('sep', r' [;,"] | $ ')

    def _build_product_rules(self):
        self.product(
            self.convert,
            r""" keyword (?P<value> (?: sex | word ){1,2} (?: quest )? ) sep
                | keyword (?P<value> (?: sex | word ) (?: quest )? )
                | (?P<value> sex (?: quest )? )
                """)

    def convert(self, token):
        """Convert parsed tokens into a result."""
        trait = Parse(
            value=token.groups['value'],
            start=token.start,
            end=token.end)
        trait.value = re.sub(r'\s*\?$', '?', trait.value, flags=self.flags)
        trait.value = re.sub(r'^m\w*', 'male', trait.value, flags=self.flags)
        trait.value = re.sub(r'^f\w*', 'female', trait.value, flags=self.flags)
        return trait
