"""Update entity data without creating new entities.

It performs matches and runs functions on those matches. The "after_match" functions
perform the actual updates.
"""

import spacy
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.util import filter_spans

from traiter.pipe_util import RejectMatch, add_spacy_extensions, relabel_entity

UPDATE_ENTITY_DATA = 'update_entity_data'

add_spacy_extensions()


@Language.factory(UPDATE_ENTITY_DATA)
def update_entity_data(nlp: Language, name: str, patterns: list[list[dict]]):
    """Create a entity data dispatch table."""
    return UpdateEntityData(nlp, name, patterns)


class UpdateEntityData:
    """Perform actions to update user defined fields etc. for all entities."""

    def __init__(self, nlp, name, patterns):
        self.nlp = nlp
        self.name = name
        self.matcher = Matcher(nlp.vocab)
        self.dispatch = self.build_dispatch_table(patterns)
        self.build_matchers(patterns)

    def build_matchers(self, patterns):
        """Setup matchers."""
        for pattern_set in patterns:
            for pattern in pattern_set:
                label = pattern['label']
                self.matcher.add(label, pattern['patterns'], greedy='LONGEST')

    @staticmethod
    def build_dispatch_table(patterns):
        """Setup after match actions."""
        dispatch = {}
        for matcher in patterns:
            for pattern_set in matcher:
                label = pattern_set['label']
                if on_match := pattern_set.get('on_match'):
                    func = on_match if isinstance(on_match, str) else on_match['func']
                    func = spacy.registry.misc.get(func)
                    dispatch[label] = func
        return dispatch

    def __call__(self, doc: Doc) -> Doc:
        entities = []
        seen = set()

        matches = self.matcher(doc, as_spans=True)
        matches = filter_spans(matches)

        for ent in matches:
            if action := self.dispatch.get(ent.label_):
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
