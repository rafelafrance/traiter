from ..pattern_compilers.matcher import Compiler
from ..term_list import TermList


class MatcherPatterns:
    def __init__(
        self,
        name: str,
        decoder: dict[str, dict],
        patterns: list[str],
        on_match: str,
        terms: TermList = None,
    ):
        self.name = name
        self.decoder = decoder
        self.patterns = patterns
        self.on_match = on_match
        self._terms = terms

    @property
    def terms(self):
        return self._terms.data

    def __call__(self):
        return self.compile()

    def compile(self):
        return Compiler(
            self.name,
            on_match=self.on_match,
            decoder=self.decoder,
            patterns=self.patterns,
        )
