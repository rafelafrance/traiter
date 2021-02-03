"""Compile strings to spacy dependency matcher patterns.

EXPERIMENTAL!

In an effort to make dependency patterns readable I've created simple compilers that
take in, hopefully, readable strings and convert them to spacy patterns using a
dictionary and some simple rules.
"""

from collections import deque

from warnings import warn

REL_OP = ' < > << >> . .* ; ;* $+ $- $++ $-- '.split()


class DependencyCompiler:
    """Convert patterns strings to spacy token pattern arrays."""

    def __init__(self, shared_dependencies: dict[str, dict] = None):
        self.shared_dependencies = shared_dependencies if shared_dependencies else {}

    def __call__(self, map_: dict[str, dict], *patterns: str) -> list[list[dict]]:
        """Convert patterns strings to spacy dependency pattern arrays."""
        map_ = map_ if map_ else {}
        # Allow map_ to overwrite shared_dependencies
        map_ = {**self.shared_dependencies, **map_}

        all_patterns = []

        for string in patterns:
            pattern_seq = []
            stack = deque()
            left_id, rel_op, right_id, right_attrs = '', '', '', {}

            for i, key in enumerate(string.split()):

                # Start a branching pattern by saving the current state
                if key == '(':
                    stack.append((left_id, rel_op))

                # Return to the previous state from a branching pattern
                elif key == ')':
                    if len(stack):
                        left_id, rel_op = stack.pop()
                    else:
                        warn(f'Unbalanced parentheses in pattern: {string}')

                # Add an operator to the queue
                elif key in REL_OP:
                    rel_op = key

                # Build the spacy dependency pattern
                elif right_attrs := map_.get(key):
                    right_id = f'{key}{i}'

                    if left_id and rel_op:
                        pattern_seq.append({
                            'LEFT_ID': left_id,
                            'REL_OP': rel_op,
                            'RIGHT_ID': right_id,
                            'RIGHT_ATTRS': right_attrs,
                        })

                    # First time is for the anchor pattern
                    elif not (left_id or rel_op):
                        pattern_seq.append({
                            'RIGHT_ID': right_id,
                            'RIGHT_ATTRS': right_attrs,
                        })

                    else:
                        warn(f'Dependency patterns go: ID op ID op ID... {string}')

                    left_id = right_id

                else:
                    warn(f'No right_attrs or rel_op for "{key}" in "{string}"')

            all_patterns.append(pattern_seq)

        return all_patterns
