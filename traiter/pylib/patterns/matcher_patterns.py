from dataclasses import dataclass
from typing import Iterable

from ..pattern_compilers.matcher import Compiler
from ..term_list import TermList


@dataclass()
class MatcherPatterns:
    """This holds data need to work with a set of patterns.

    name:     The name of this set of patterns.
    decoder:  Use this decoder to compile the patterns.
    patterns: The patterns to compile.
    on_match: The registered function to execute when matching.
    terms:    The list of terms this matcher uses.
    replace:  This is a convenience function, we use this field from term list a lot.
    keep:     These labels are considered full matches, other labels are partial terms
              and should be deleted before outputting the results
    """

    name: str
    on_match: str | None
    decoder: dict[str, dict]
    patterns: list[str]
    terms: TermList | None
    keep: list[str] | None

    @property
    def replace(self):
        return self.terms.replace

    def compile(self):
        return Compiler(
            self.name,
            on_match=self.on_match,
            decoder=self.decoder,
            patterns=self.patterns,
        )

    def as_dict(self) -> dict:
        return {
            "label": self.name,
            "on_match": self.on_match,
            "patterns": self.patterns,
        }

    @staticmethod
    def all_terms(patterns: Iterable["MatcherPatterns"]) -> TermList:
        combined_terms = TermList()
        for pattern in patterns:
            if pattern.terms:
                combined_terms += pattern.terms
        return combined_terms

    @staticmethod
    def all_keeps(patterns: Iterable["MatcherPatterns"]) -> list[str]:
        keep = []
        for pattern in patterns:
            if pattern.keep:
                keep += pattern.keep
        return sorted(set(keep))
