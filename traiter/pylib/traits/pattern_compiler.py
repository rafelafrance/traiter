"""Compile strings to spacy matcher patterns.

In an effort to make patterns more readable I've created simple compilers that take in,
hopefully, readable strings and convert them to spacy patterns using a dictionary and
some simple rules.
"""
import copy
import re
from warnings import warn


class Compiler:
    def __init__(
        self,
        *,
        label: str,
        patterns: list[str],
        decoder: dict[str, dict],
        on_match: str | None = None,
        id: str = "",  # noqa
    ):
        self.label = label
        self.raw_patterns = patterns
        self.decoder = decoder
        self.on_match = on_match
        self.patterns = []
        self.id = id

    def compile(self):
        """Convert raw patterns strings to spacy matcher pattern arrays."""
        for string in self.raw_patterns:
            pattern_seq = []

            for key in string.split():
                token = self.decoder.get(key)

                if token is None:
                    token = self.decoder.get(key[:-1])
                    if key[-1] in "?*+!" and token is not None:
                        token = copy.copy(token)
                        token["OP"] = key[-1]

                    elif key[-1] == "}" and (match := re.search(r"{[\d,]+}$", key)):
                        token = self.decoder.get(key[: match.start()])
                        if token is not None:
                            token = copy.copy(token)
                            token["OP"] = match.group()

                if token is not None:
                    pattern_seq.append(token)
                else:
                    warn(f'No token pattern for "{key}" in "{string}"')

            self.patterns.append(pattern_seq)

        return self
