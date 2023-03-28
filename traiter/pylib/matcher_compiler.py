"""Compile strings to spacy matcher patterns.

EXPERIMENTAL!

In an effort to make patterns more readable I've created simple compilers that take in,
hopefully, readable strings and convert them to spacy patterns using a dictionary and
some simple rules.
"""
import re
from copy import deepcopy
from typing import Any
from typing import Callable
from warnings import warn

from spacy.tokens.doc import Doc

from .util import as_list

_Ruler = Callable[[Doc], Doc]
_Pattern = str | list[str], list[list[dict[str, Any]]]


class Compiler:
    def __init__(self, label: str, *, patterns: _Pattern, decoder: dict[str, dict]):
        self.label = label
        self.patterns = patterns
        patterns2 = as_list(patterns)
        self.patterns = self.compile(patterns2, decoder)

    @staticmethod
    def compile(
        patterns: list[str], decoder: dict[str, dict]
    ) -> list[list[dict[str, Any]]]:
        """Convert patterns strings to spacy matcher pattern arrays."""
        all_patterns = []

        for string in patterns:
            pattern_seq = []

            for key in string.split():
                token = deepcopy(decoder.get(key))
                op = key[-1]

                if not token and op in "?*+!":
                    token = deepcopy(decoder.get(key[:-1]))
                    token["OP"] = op
                elif not token and op == "}":
                    if match := re.search(r"{[\d,]+}$", key):
                        op = match.group()
                        token = deepcopy(decoder.get(key[: match.start()]))
                        token["OP"] = op

                if token:
                    pattern_seq.append(token)
                else:
                    warn(f'No token pattern for "{key}" in "{string}"')

            all_patterns.append(pattern_seq)

        return all_patterns
