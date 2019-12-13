"""Common logic for parsing trait notations."""

from typing import Callable, List
from pylib.stacked_regex.parser import Parser
from pylib.stacked_regex.rule import Rules
from pylib.vertnet.trait import Trait


def fix_up_nop(trait, text):  # pylint: disable=unused-argument
    """Fix problematic parses."""
    return trait


class Base(Parser):  # pylint: disable=too-few-public-methods
    """Shared lexer logic."""

    def __init__(
            self, rules: Rules,
            name: str = 'parser',
            fix_up: Callable[[Trait, str], Trait] = None) -> None:
        """Build the trait parser."""
        super().__init__(name=name, rules=rules)
        self.fix_up = fix_up if fix_up else fix_up_nop

    # pylint: disable=arguments-differ
    def parse(self, text: str, field: str = None) -> List[Trait]:
        """Find the traits in the text."""
        traits = []

        tokens = super().parse(text)

        for token in tokens:

            trait_list = token.action(token)

            # The action function can reject the token
            if not trait_list:
                continue

            # Some parses represent multiple traits, fix them all up
            if not isinstance(trait_list, list):
                trait_list = [trait_list]

            # Add the traits after any fix up.
            for trait in trait_list:
                trait = self.fix_up(trait, text)
                if trait:  # The parse may fail during fix up
                    if field:
                        trait.field = field
                    traits.append(trait)

        return traits


def convert(token):
    """Convert parsed tokens into a result."""
    return Trait(
        value=token.groups['value'].lower(),
        start=token.start, end=token.end)
