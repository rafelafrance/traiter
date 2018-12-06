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

    sentinel_token = {'token': '__END__', 'value': None, 'start': 0, 'end': 0}

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


def build(regex, boundary=True):
    r"""
    Build a lexer regular expression.

    This will be used to build up the '|' (regex pipe) sections of the full
    parser regex. That is, this is one clause between the pipes. Like so:
        ... | clause | ...

    boundary: True or False
        If boundary is True then the regex will be wrapped in \b so that only
        the entire word will be matched. See re documentation.
        - This is helpful for keyword searches like 't'
          which would match every 't' in the input but wrapping the regex in
          \b will only match a t standing on its own.
        - It is not helpful for searching for things like '19mm' where there is
          no word break between the two tokens.
        - It is also not helpful if your pattern ends or starts with a non-word
          character.
    """
    if boundary:
        return r'\b ( {} ) \b'.format(regex)
    return regex
