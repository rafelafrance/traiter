"""Tokenize the notations."""

# pylint: disable=too-few-public-methods

import re
from lib.lexers.util import boundary


class Base:
    """Shared lexer logic."""

    def __init__(self):
        """Compile the regex."""
        joined = ' | '.join([f' (?P<{k}> {v} ) ' for k, v in self.tokens])
        self.regex = re.compile(joined, re.VERBOSE | re.IGNORECASE)

    def tokenize(self, raw):
        """Split the text into tokens."""
        tokens = []

        for match in self.regex.finditer(raw):

            for key, _ in self.tokens:
                if match[key] is not None:
                    tokens.append({
                        'token': key,
                        'value': match[0],
                        'start': match.start(),
                        'end': match.end()})
                    break

        return tokens

    # For our purposes numbers are always positive and decimals
    number = ('number',
              r' (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? ')

    to = ('to', r' - | to ')              # Used to parse numeric ranges

    cross = ('cross', r'  x | by | \* ')  # Used to parse length x width values

    word = ('word', boundary(r' \w+ '))   # Generic word

    stop = ('stop', r' [.;] ')  # Used to separate key1=value1; key2=val2 pairs

    # Order matters!
    tokens = [number, to, cross, word, stop]

    sentinel_token = {'token': 'END', 'value': None, 'start': 0, 'end': 0}
