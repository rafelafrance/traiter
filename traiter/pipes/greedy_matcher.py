"""A matcher pipe that overwrites entities with the longest non-overlapping matches."""

from typing import Dict, List

import spacy
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc


@Language.factory('greedy_matcher')
def greedy_matcher(nlp: Language, name: str, patterns: List[List[Dict]]):
    """Build a matcher pipe that creates a list of non-overlapping entities."""
    return GreedyMatcher(nlp.vocab, patterns)


class GreedyMatcher:
    """A matcher pipe that creates a list of non-overlapping entities."""

    def __init__(self, vocab, patterns):
        self.matcher = Matcher(vocab)
        for pattern_set in patterns:
            for pattern in pattern_set:
                label = pattern['label']
                on_match = spacy.registry.misc.get(pattern['on_match'])
                self.matcher.add(
                    label, pattern['patterns'], on_match=on_match, greedy='LONGEST')

    def __call__(self, doc: Doc) -> Doc:
        spans = self.matcher(doc, as_spans=True)

        seen = set()
        for span in spans:
            seen.update(range(span.start, span.end))

        for span in doc.ents:
            if span.start not in seen and span.end - 1 not in seen:
                spans.append(span)

        ents = sorted(spans, key=lambda e: e.start)
        doc.ents = ents
        return doc
