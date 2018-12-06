"""Tokenize the notations."""

import re


class BaseLexer:
    """Shared lexer logic."""

    # For our purposes numbers are always positive and decimals
    number = ('number',
              r' (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? ')

    to = ('to', r' - | to ')    # Used to parse numeric ranges

    cross = ('cross', r'  x | by | \* ')  # Used to parse length x width values

    word = ('word', r' \w+ ')   # Generic word

    stop = ('stop', r' [.;] ')  # Used to separate key1=value1; key2=val2 pairs

    # Order matters!
    tokens = [number, to, cross, word, stop]

    def __init__(self):
        """Compile the regex."""
        joined = ' | '.join([f' (?P<{k}> {v} ) ' for k, v in self.tokens])
        self.regex = re.compile(joined, re.VERBOSE | re.IGNORECASE)

    def tokenize(self, input):
        """Split the text into tokens."""
        tokens = []

        for match in self.regex.finditer(input):

            for key, _ in self.tokens:
                if match[key] is not None:
                    tokens.append({
                        'token': key,
                        'value': match[0],
                        'start': match.start(),
                        'end': match.end()})
                    break

        return tokens


def isolate(regex):
    return r'\b ( {} ) \b'.format(regex)
