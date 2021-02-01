"""Actions for enriching entities with new data."""

from typing import Dict

from spacy.language import Language
from spacy.tokens import Doc

from ..pipe_util import RejectMatch, add_spacy_extensions, get_action, relabel_entity

ADD_ENTITY_DATA = 'add_entity_data'

add_spacy_extensions()


@Language.factory(ADD_ENTITY_DATA)
def add_entity_data(nlp: Language, name: str, actions: Dict[str, str]):
    """Create a entity data dispatch table."""
    return AddEntityData(actions)


class AddEntityData:
    """Perform actions to fill user defined fields etc. for all entities."""

    def __init__(self, actions: Dict[str, str]):
        self.dispatch = {k: get_action(v) for k, v in actions.items()}

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
