"""Compile strings to spacy matcher patterns.

EXPERIMENTAL!

In an effort to make patterns more readable I've created simple compilers that take in,
hopefully, readable strings and convert them to spacy patterns using a dictionary and
some simple rules.
"""
from copy import deepcopy
from typing import Callable
from typing import Optional
from typing import Union
from warnings import warn

from spacy.pipeline import EntityRuler
from spacy.tokens.doc import Doc

from ..util import as_list
from .compilers import CompilerPatterns
from .compilers import Decoder
from .compilers import PatternArg
from .compilers import SpacyPatterns

RulerType = Union[EntityRuler, Callable[[Doc], Doc]]


class MatcherCompiler:
    """Pattern object for rule-based matchers."""

    def __init__(
        self,
        label: str,
        *,
        patterns: PatternArg,
        decoder: Optional[Decoder] = None,
        on_match: Optional[str] = None,
        id_: str = "",
    ):
        self.label = label
        self.on_match = on_match
        self.patterns = patterns
        self.id = id_

        if decoder:
            patterns2 = as_list(patterns)
            self.patterns = self.compile(patterns2, decoder)

    def as_dict(self) -> dict:
        """Return the object as a serializable dict."""
        return {
            "label": self.label,
            "on_match": self.on_match,
            "patterns": self.patterns,
            "id": self.id,
        }

    @staticmethod
    def compile(patterns: CompilerPatterns, decoder: Decoder) -> SpacyPatterns:
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

                if token:
                    pattern_seq.append(token)
                else:
                    warn(f'No token pattern for "{key}" in "{string}"')

            all_patterns.append(pattern_seq)

        return all_patterns


Compilers = Union[MatcherCompiler, list[MatcherCompiler]]


def as_dicts(patterns: Compilers) -> list[dict]:
    """Convert all patterns to a dicts."""
    return [p.as_dict() for p in as_list(patterns)]


def compile_ruler_patterns(ruler: RulerType, patterns: Compilers) -> None:
    """Rename add_ruler_patterns."""
    add_ruler_patterns(ruler, patterns)


def add_ruler_patterns(ruler: RulerType, patterns: Compilers) -> None:
    """Add patterns to a ruler."""
    patterns = as_list(patterns)
    rules = []
    for matcher in patterns:
        label = matcher.label
        id_ = matcher.id
        for pattern in matcher.patterns:
            rule = {"label": label, "pattern": pattern}
            if id_:
                rule["id"] = id_
            rules.append(rule)
    ruler.add_patterns(rules)


def patterns_to_dispatch(patterns: Compilers) -> dict[str, str]:
    """Convert patterns to a dispatch table."""
    dispatch = {p.label: p.on_match for p in as_list(patterns) if p.on_match}
    return dispatch
