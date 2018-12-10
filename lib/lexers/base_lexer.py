"""Tokenize the notations."""

# pylint: disable=too-few-public-methods

import re


class BaseLexer:
    """Shared lexer logic."""

    # For our purposes numbers are always positive and decimals
    number = ('number',
              r' (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ ) (?: \. \d+ )? ')

    to = ('to', r' - | to ')              # Used to parse numeric ranges

    cross = ('cross', r'  x | by | \* ')  # Used to parse length x width values

    word = ('word', r' \w+ ')             # Generic word

    stop = ('stop', r' [.;] ')  # Used to separate key1=value1; key2=val2 pairs

    # Order matters!
    tokens = [number, to, cross, word, stop]

    sentinel_token = {'token': 'END', 'value': None, 'start': 0, 'end': 0}

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


def isolate(regex):
    r"""Wrap a regular expression in \b character class.

    This is used to "isolate" a word on a word boundary so the regex does not
    match the interior of a word.

    - This is helpful for keyword searches like 't'. Without this 't' would
      match both 't's in 'that' but the regex in \b neither 't' is matched.
      Only 't's like ' t ', or '$t.', etc. will match.
    - It is not helpful for searching for things like '19mm' where there is
      no word break between the two tokens.
    - It is also not helpful if your pattern ends or starts with a non-word
      character.
    """
    return r'\b (?: {} ) \b'.format(regex)
