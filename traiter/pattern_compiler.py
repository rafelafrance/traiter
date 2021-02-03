"""Compile strings to spacy matcher patterns.

EXPERIMENTAL!

In an effort to make patterns readable I've created simple compilers that take in,
hopefully, readable strings and convert them to spacy patterns using a dictionary and
some simple rules.
"""

from copy import deepcopy
from warnings import warn

REL_OP = ' < > << >> . .* ; ;* $+ $- $++ $-- '.split()


class PatternCompiler:
    """Convert patterns strings to spacy token pattern arrays."""

    def __init__(
            self,
            shared_patterns: dict[dict] = None,
            shared_dependencies: dict[dict] = None
    ):
        self.shared_patterns = shared_patterns if shared_patterns else {}
        self.shared_dependencies = shared_dependencies if shared_dependencies else {}

    def to_patterns(self, map_: dict[str, dict], *patterns: str) -> list[list[dict]]:
        """Convert patterns strings to spacy token pattern arrays."""
        map_ = map_ if map_ else {}
        # We want the arg to overwrite shared_patterns
        map_ = {**self.shared_patterns, **map_}

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

    # TODO Handle branching patterns
    def to_dependencies(
            self, map_: dict[str, dict], *patterns: str) -> list[list[dict]]:
        """Convert patterns strings to spacy dependency pattern arrays."""
        map_ = map_ if map_ else {}
        # We want the arg to overwrite shared_patterns
        map_ = {**self.shared_dependencies, **map_}

        all_patterns = []

        for string in patterns:
            pattern_seq = []
            left_id, rel_op, right_id, right_attrs = '', '', '', {}

            for i, key in enumerate(string.split()):

                if key in REL_OP:
                    rel_op = key

                elif right_attrs := map_.get(key):
                    right_id = f'{key}{i}'

                    if left_id and rel_op:
                        pattern_seq.append({
                            'LEFT_ID': left_id,
                            'REL_OP': rel_op,
                            'RIGHT_ID': right_id,
                            'RIGHT_ATTRS': right_attrs,
                        })

                    elif not (left_id or rel_op):
                        pattern_seq.append({
                            'RIGHT_ID': right_id,
                            'RIGHT_ATTRS': right_attrs,
                        })
                    else:
                        warn(f'Dependency patterns must go: ID op ID op ID... {string}')

                    left_id = right_id

                else:
                    warn(f'No right_attrs or rel_op for "{key}"')

            all_patterns.append(pattern_seq)

        return all_patterns
