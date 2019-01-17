"""Parse sex notations."""

import re
from lib.trait import Trait
from lib.parsers.base import Base


class Sex(Base):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.kwd('keyword', 'sex')

        self.kwd('sex', r' females? | males? | f | m')
        self.lit('quest', r' \? ')

        # These are words that indicate that "sex" is not a key
        self.kwd('skip', r' and | is | was ')

        self.lit('word', r' [a-z]\S+ ')

        # Build a rules for parsing the trait
        self.product(
            self.convert,
            r""" keyword (?P<value> (?: sex | word ) quest )
                | keyword (?P<value> sex | word )
                | (?P<value> sex quest )
                | (?P<value> sex )
                """)

        self.finish_init()

    def convert(self, token):
        """Convert parsed tokens into a result."""
        trait = Trait(
            value=token.groups['value'],
            start=token.start,
            end=token.end)
        trait.value = re.sub(r'\s*\?$', '?', trait.value, flags=self.flags)
        trait.value = re.sub(r'^m\w*', r'male', trait.value, flags=self.flags)
        trait.value = re.sub(
            r'^f\w*', r'female', trait.value, flags=self.flags)
        return trait
