"""Tokenize the notations."""

import re


class BaseLexer:
    """Shared lexer logic."""

    # For our purposes numbers are always positive and decimals
    number = ('number',
              r' (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? ')
    word = ('word', r' \w+ ')

    # Order matters
    forms = [number, word]

    def __init__(self):
        """Compile the regex."""
        joined = ' | '.join([f' (?P<{k}> {v} ) ' for k, v in self.forms])
        self.regex = re.compile(joined, re.VERBOSE | re.IGNORECASE)

    def tokenize(self, input):
        """Split the text into tokens."""
        tokens = []

        for match in self.regex.finditer(input):

            for key, _ in self.forms:
                if match[key] is not None:
                    tokens.append((key, match[0], match.start(), match.end()))
                    break

        return tokens
