"""Common logic for parsing trait notations."""

import re
from stacked_regex.stacked_regex import StackedRegex
from traiter.util import ordinal


class BaseTrait(StackedRegex):
    """Shared lexer logic."""

    flags = re.VERBOSE | re.IGNORECASE

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__()

        self.args = args
        self.shared_token = self.from_tuple

    def parse(self, text, field=''):
        """Find the traits in the text.

        We get the trait list from the StackedRegex engine & then fix them up
        afterwards.
        """
        traits = []

        for token in self.match(text):

            trait = self.regexps[token.name].action(token)

            # The function can reject the token
            if not trait:
                continue

            # Some parses represent multiple traits, fix them all up
            if not isinstance(trait, list):
                trait = [trait]

            # Add the traits after any fix up.
            for single_trait in trait:
                trait = self.fix_up_trait(single_trait, text)
                if trait:
                    single_trait.field = field
                    traits.append(single_trait)

        return traits

    def fix_up_trait(self, trait, text):
        """Fix problematic parses."""
        return trait

    @staticmethod
    def csv_formatter(trait, row, parses):
        """Format the trait for CSV output."""
        records = {}
        for parse in parses:
            key = parse.as_key()
            if key not in records:
                records[key] = parse

        for i, parse in enumerate(records.values(), 1):
            row[f'{trait}:{ordinal(i)}_{trait}_notation'] = parse.value

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        return False

    @staticmethod
    def adjust_record(data, trait):
        """Adjust the trait based on other fields."""
