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
from typing import Optional
from typing import Union
from warnings import warn

from spacy.tokens.doc import Doc

from ..util import as_list

_Ruler = Callable[[Doc], Doc]
_Pattern = Union[str, list[str], list[list[dict[str, Any]]]]


class Compiler:
    def __init__(
        self,
        label: str,
        *,
        patterns: _Pattern,
        decoder: Optional[dict[str, dict]] = None,
        on_match: Optional[str] = None,
    ):
        self.label = label
        self.on_match = on_match
        self.patterns = patterns

        if decoder:
            patterns2 = as_list(patterns)
            self.patterns = self.compile(patterns2, decoder)

    def as_dict(self) -> dict:
        return {
            "label": self.label,
            "on_match": self.on_match,
            "patterns": self.patterns,
        }

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

    @staticmethod
    def as_dicts(patterns) -> list[dict]:
        """Convert all patterns to a dicts."""
        return [p.as_dict() for p in as_list(patterns)]
