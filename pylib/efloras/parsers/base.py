"""Common logic for parsing trait notations."""

import re
import pylib.stacked_regex.stacked_regex as stacked


class Base(stacked.Parser):  # pylint: disable=too-few-public-methods
    """Shared lexer logic."""

    def parse(self, text):
        """Find the traits in the text."""
        all_traits = []

        tokens = super().parse(text)

        for token in tokens:

            traits = token.action(token)

            # The action function may reject the token
            if not traits:
                continue

            all_traits += traits if isinstance(traits, list) else [traits]

        return all_traits


def split_attrs(data):
    """Split the text blob into attributes."""
    attrs = [x for x in re.split(r'\s*[,;:]\s*', data) if x]
    attrs[-1] = re.sub(r'\s*\.\s*$', '', attrs[-1])
    return attrs
