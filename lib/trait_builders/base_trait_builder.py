"""Common logic for parsing trait notations."""

from stacked_regex.stacked_regex import StackedRegex
import lib.writers.csv_formatters.base_trait_csv_formatter as \
    base_trait_csv_formatter


class BaseTraitBuilder(StackedRegex):
    """Shared lexer logic."""

    csv_formatter = base_trait_csv_formatter.csv_formatter

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__()

        self.args = args
        self.shared_token = self.from_tuple

    def parse(self, text, field=None):
        """Find the trait_builders in the text.

        We get the trait list from the StackedRegex engine & then fix them up
        afterwards.
        """
        traits = []

        for token in self.match(text):

            trait_list = self.regexps[token.name].action(token)

            # The action function can reject the token
            if not trait_list:
                continue

            # Some parses represent multiple trait_builders, fix them all up
            if not isinstance(trait_list, list):
                trait_list = [trait_list]

            # Add the traits after any fix up.
            for trait in trait_list:
                trait = self.fix_problem_parses(trait, text)
                if trait:  # The parse may fail during fix up
                    if field:
                        trait.field = field
                    traits.append(trait)

        return traits

    def fix_problem_parses(self, trait, text):
        """Fix problematic parses."""
        return trait

    @staticmethod
    def should_skip(data, trait):
        """
        Check if this record should be skipped because of other fields.

        For instance, we skip parsing testes traits for females.
        """
        return False

    @staticmethod
    def adjust_record(data, trait):
        """Adjust the trait based on other fields."""
