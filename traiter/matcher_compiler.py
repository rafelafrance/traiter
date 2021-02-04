"""Compile strings to spacy matcher patterns.

EXPERIMENTAL!

In an effort to make patterns readable I've created simple compilers that take in,
hopefully, readable strings and convert them to spacy patterns using a dictionary and
some simple rules.
"""

from copy import deepcopy
from traceback import print_exc
from warnings import warn


class MatcherCompiler:
    """Convert patterns strings to spacy token pattern arrays."""

    def __init__(self, decoder: dict[str, dict]):
        self.decoder = decoder

    def __call__(self, *patterns: str) -> list[list[dict]]:
        """Convert patterns strings to spacy token pattern arrays."""
        all_patterns = []

        for string in patterns:
            pattern_seq = []

            for key in string.split():
                token = deepcopy(self.decoder.get(key))
                op = key[-1]

                if not token and op in '?*+!':
                    token = deepcopy(self.decoder.get(key[:-1]))
                    token['OP'] = op

                if token:
                    pattern_seq.append(token)
                else:
                    print_exc()
                    warn(f'No token pattern for "{key}"')

            all_patterns.append(pattern_seq)

        return all_patterns
