"""Add dependency matcher pipe to the pipeline."""

from typing import Dict, List

import spacy
from spacy.language import Language
from spacy.matcher import DependencyMatcher


@Language.factory('dependency')
def dependency(nlp: Language, name: str, patterns: List[Dict]):
    """Build a dependency pipe."""
    return Dependency(nlp.vocab, patterns)


class Dependency:
    """Matchers that walk the parse tree of a sentence or doc."""

    def __init__(self, vocab, patterns):
        self.matcher = DependencyMatcher(vocab)
        for pattern in patterns:
            on_match = spacy.registry.misc.get(pattern['on_match'])
            self.matcher.add(pattern['label'], pattern['patterns'], on_match=on_match)

    def __call__(self, doc):
        self.matcher(doc)
        return doc
