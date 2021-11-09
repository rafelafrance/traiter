"""Compile strings to spacy dependency matcher patterns.

EXPERIMENTAL!

In an effort to make dependency patterns more readable I've created simple compilers
that take in, hopefully, readable strings and convert them to spacy patterns using a
dictionary and some simple rules.
"""

from collections import deque
from typing import Any, Optional
from warnings import warn

from traiter.patterns.patterns import (
    CompilerPatterns, Decoder, PatternArg, SpacyPatterns)
from traiter.util import as_list

REL_OP = ' < > << >> . .* ; ;* $+ $- $++ $-- '.split()

OnMatchWithArgs = dict[str, Any]


class DependencyPatterns:
    """Convert patterns strings to spacy token pattern arrays."""

    def __init__(
            self,
            label: str,
            *,
            patterns: PatternArg,
            decoder: Optional[Decoder] = None,
            on_match: OnMatchWithArgs):
        self.decoder = decoder
        self.label = label
        self.decoder = decoder
        self.on_match = on_match

        if decoder:
            patterns2 = as_list(patterns)
            self.patterns: SpacyPatterns = self.compile(patterns2)

    def as_dict(self) -> dict:
        """Return the object as a serializable dict."""
        return {
            'label': self.label,
            'on_match': self.on_match,
            'patterns': self.patterns}

    def compile(self, patterns: CompilerPatterns) -> SpacyPatterns:
        """Convert patterns strings to spacy dependency pattern arrays."""
        all_patterns = []

        for string in patterns:
            pattern_seq = []
            stack: deque = deque()
            left_id, rel_op, right_id = '', '', ''

            # Parens can be contiguous with the a symbol or operator
            new_str = string.replace('(', ' ( ').replace(')', ' ) ')

            for i, key in enumerate(new_str.split()):

                # Start a branching pattern by saving the current state
                if key == '(':
                    # Allow nested fragment to start with either an ID or an OP
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
                elif self.decoder and (right_attrs := self.decoder.get(key)):
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
                        warn(f"Dependency patterns don't start with an op... {string}")

                    left_id = right_id

                else:
                    warn(f'No right_attrs or rel_op for "{key}" in "{string}"')

            all_patterns.append(pattern_seq)

        return all_patterns
