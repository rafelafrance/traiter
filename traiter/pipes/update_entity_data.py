"""Update entity data without creating new entities.

It performs matches and runs functions on those matches. The "after_match" functions
perform the actual updates.
"""

from typing import Dict, List

import spacy
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.util import filter_spans

from traiter.pipe_util import RejectMatch, add_spacy_extensions, relabel_entity

UPDATE_ENTITY_DATA = 'update_entity_data'

add_spacy_extensions()


@Language.factory(UPDATE_ENTITY_DATA)
def update_entity_data(nlp: Language, name: str, patterns: List[List[Dict]]):
    """Create a entity data dispatch table."""
    return UpdateEntityData(nlp, patterns)


class UpdateEntityData:
    """Perform actions to update user defined fields etc. for all entities."""

    def __init__(self, nlp, patterns):
        self.nlp = nlp
        self.matcher = Matcher(nlp.vocab)
        self.after_match = self.build_after_match(patterns)
        self.build_matchers(patterns)

    def build_matchers(self, patterns):
        """Setup matchers."""
        for pattern_set in patterns:
            for pattern in pattern_set:
                label = pattern['label']
                on_match = pattern.get('on_match')
                on_match = spacy.registry.misc.get(on_match) if on_match else None
                self.matcher.add(
                    label, pattern['patterns'], on_match=on_match, greedy='LONGEST')

    @staticmethod
    def build_after_match(patterns):
        """Setup after match actions."""
        after_match = {}
        for matcher in patterns:
            for pattern_set in matcher:
                if after := pattern_set.get('after_match'):
                    func = spacy.registry.misc.get(after['func'])
                    after_match[pattern_set['label']] = func
        return after_match

    def __call__(self, doc: Doc) -> Doc:
        entities = []
        seen = set()

        matches = self.matcher(doc, as_spans=True)
        matches = filter_spans(matches)

        for ent in matches:
            if action := self.after_match.get(ent.label_):
                try:
                    action(ent)
                except RejectMatch:
                    continue

            for sub_ent in ent.ents:
                label = sub_ent.label_
                sub_ent, label = relabel_entity(sub_ent, label)
                sub_ent._.data['trait'] = label
                entities.append(sub_ent)
                seen.update(range(sub_ent.start, sub_ent.end))

        for ent in doc.ents:
            if ent.start not in seen and ent.end - 1 not in seen:
                entities.append(ent)

        doc.ents = sorted(entities, key=lambda s: s.start)
        return doc
