"""Compile strings to spacy matcher patterns.

EXPERIMENTAL!

In an effort to make patterns readable I've created simple compilers that take in,
hopefully, readable strings and convert them to spacy patterns using a dictionary and
some simple rules.
"""

from copy import deepcopy
from warnings import warn


class PatternCompiler:
    """Convert patterns strings to spacy token pattern arrays."""

    def __init__(self, shared_patterns: dict[dict] = None):
        self.shared = shared_patterns if shared_patterns else {}

    def to_patterns(self, map_: dict[str, dict], *patterns: str):
        """Convert patterns strings to spacy token pattern arrays."""
        map_ = map_ if map_ else {}
        map_ = {**self.shared, **map_}  # We want the arg to overwrite shared_patterns

        all_patterns = []

        for string in patterns:
            pattern_seq = []

            for key in string.split():
                token = deepcopy(map_.get(key))
                op = key[-1]

                if not token and op in '?*+!':
                    token = deepcopy(map_.get(key[:-1]))
                    token['OP'] = op

                if token:
                    pattern_seq.append(token)
                else:
                    warn(f'No token pattern for "{key}"')

            all_patterns.append(pattern_seq)

        return all_patterns
