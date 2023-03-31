"""Compile strings to spacy matcher patterns.

In an effort to make patterns more readable I've created simple compilers that take in,
hopefully, readable strings and convert them to spacy patterns using a dictionary and
some simple rules.
"""
import re
from copy import deepcopy
from warnings import warn


class Compiler:
    def __init__(
        self,
        label: str,
        *,
        patterns: list[str],
        decoder: dict[str, dict],
        id: str = "",  # noqa
    ):
        self.label = label
        self.id = id
        self.raw_patterns = patterns
        self.decoder = decoder
        self.patterns = None

    def compile(self, force=False) -> None:
        """Convert raw patterns strings to spacy matcher pattern arrays."""
        if self.patterns and not force:
            return

        for string in self.raw_patterns:
            pattern_seq = []

            for key in string.split():
                token = deepcopy(self.decoder.get(key))
                op = key[-1]

                if not token and op in "?*+!":
                    token = deepcopy(self.decoder.get(key[:-1]))
                    token["OP"] = op
                elif not token and op == "}":
                    if match := re.search(r"{[\d,]+}$", key):
                        op = match.group()
                        token = deepcopy(self.decoder.get(key[: match.start()]))
                        token["OP"] = op

                if token:
                    pattern_seq.append(token)
                else:
                    warn(f'No token pattern for "{key}" in "{string}"')

            self.patterns.append(pattern_seq)
