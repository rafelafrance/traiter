"""Compile strings to spacy dependency matcher patterns.

EXPERIMENTAL!

In an effort to make dependency patterns moire readable I've created simple compilers
that take in, hopefully, readable strings and convert them to spacy patterns using a
dictionary and some simple rules.
"""

from collections import deque
from typing import Any, Union
from warnings import warn

from spacy import registry

REL_OP = ' < > << >> . .* ; ;* $+ $- $++ $-- '.split()


class DependencyPatterns:
    """Convert patterns strings to spacy token pattern arrays."""

    def __init__(
            self,
            label: str,
            *,
            patterns: Union[str, list[str]],
            decoder: dict[str, dict] = None,
            on_match: dict[str, Any]):
        self.decoder = decoder
        self.label = label
        self.decoder = decoder
        self.patterns = self.compile(patterns)
        self.on_match = on_match

        if callable(on_match['func']):
            registry.misc.register(name=label, func=on_match)
            self.on_match['func'] = label

    def as_dict(self) -> dict:
        """Return the object as a serializable dict."""
        return {
            'label': self.label,
            'on_match': self.on_match,
            'patterns': self.patterns,
        }

    def compile(self, patterns: list[str]) -> list[list[dict]]:
        """Convert patterns strings to spacy dependency pattern arrays."""
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
                elif right_attrs := self.decoder.get(key):
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
                        warn(f'Dependency patterns do not start with an op... {string}')

                    left_id = right_id

                else:
                    warn(f'No right_attrs or rel_op for "{key}" in "{string}"')

            all_patterns.append(pattern_seq)

        return all_patterns
