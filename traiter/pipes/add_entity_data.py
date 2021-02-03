"""Actions for enriching entities with new data."""

import spacy
from spacy.language import Language
from spacy.tokens import Doc

from ..pipe_util import RejectMatch, add_spacy_extensions, relabel_entity

ADD_ENTITY_DATA = 'add_entity_data'

add_spacy_extensions()


@Language.factory(ADD_ENTITY_DATA)
def add_entity_data(nlp: Language, name: str, patterns: list[list[dict]]):
    """Create a entity data dispatch table."""
    return AddEntityData(nlp, name, patterns)


class AddEntityData:
    """Perform actions to fill user defined fields etc. for all entities."""

    def __init__(self, nlp, name, patterns):
        self.nlp = nlp
        self.name = name
        self.dispatch = self.build_dispatch_table(patterns)

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

        for ent in doc.ents:
            label = ent.label_

            if action := self.dispatch.get(label):
                try:
                    action(ent)
                except RejectMatch:
                    continue

                ent, label = relabel_entity(ent, label)

            ent._.data['trait'] = label
            ent._.data['start'] = ent.start_char
            ent._.data['end'] = ent.end_char
            entities.append(ent)

        doc.ents = entities
        return doc
