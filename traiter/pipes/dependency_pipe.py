"""Add dependency matcher pipe to the pipeline."""

from typing import Dict, List, Union

import spacy
from spacy.language import Language
from spacy.matcher import DependencyMatcher


@Language.factory('dependency')
def dependency(
        nlp: Language,
        name: str,
        label: str,
        patterns: List[List[Dict[str, Union[str, Dict]]]],
        on_match
):
    """Build a dependency pipe."""
    return DependencyPipe(nlp.vocab, label, patterns, on_match)


class DependencyPipe:
    """Matchers that walk the parse tree of a sentence or doc."""

    def __init__(self, vocab, label, patterns, on_match):
        self.vocab = vocab
        self.matcher = DependencyMatcher(vocab)
        self.on_match = spacy.registry.misc.get(on_match)
        self.matcher.add(label, patterns)

    def __call__(self, doc):
        matches = self.matcher(doc)
        print(len(matches))
        for match_id, indexes in matches:
            print(self.vocab.strings[match_id])
            for idx in indexes:
                print(doc[idx])
        return doc
