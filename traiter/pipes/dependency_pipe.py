"""Add dependency matcher pipe to the pipeline."""

from collections import defaultdict
from typing import Dict, List

from spacy.language import Language
from spacy.matcher import DependencyMatcher
from spacy.tokens import Doc

DependencyType = Dict[str, List]


class DependencyPipe:
    """Matchers that walk the parse tree of a sentence or doc."""

    def __init__(self, nlp: Language, patterns: DependencyType):
        self.matcher = DependencyMatcher(nlp.vocab)
        for label, pattern_list in patterns.items():
            print(label, pattern_list)
            self.matcher.add(label, pattern_list)

    def __call__(self, doc: Doc) -> Doc:
        for sent in doc.sents:
            matches = self.matcher(sent)
            print(sent)
            print(matches)

        return doc

    @classmethod
    def add_pipe(
            cls, nlp: Language, patterns: DependencyType, name: str, **kwargs
    ) -> None:
        """Build rule matchers that recognize traits."""
        kwargs = {'last': True} if not kwargs else kwargs
        matcher = cls(nlp, patterns)
        nlp.add_pipe(matcher, name=name, **kwargs)

    @staticmethod
    def dependency_patterns(*patterns) -> DependencyType:
        """Build a single dict of dependency patterns from a list of them."""
        combined = defaultdict(list)
        for pattern_arg in patterns:
            for pattern_item in pattern_arg:
                for label, pattern_list in pattern_item.items():
                    combined[label] += pattern_list
        return combined
