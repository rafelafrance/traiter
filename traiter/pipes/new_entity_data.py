"""Actions for enriching entities with new data."""

from typing import Dict

from spacy.language import Language
from spacy.tokens import Doc

from ..entity_data_util import RejectMatch, add_extensions, get_action, relabel_entity

NEW_ENTITY_DATA = 'new_entity_data'

add_extensions()


@Language.factory(NEW_ENTITY_DATA)
def new_entity_data(nlp: Language, name: str, actions: Dict[str, str]):
    """Create a entity data dispatch table."""
    return NewEntityData(actions)


class NewEntityData:
    """Perform actions to fill user defined fields etc. for all entities."""

    def __init__(self, actions: Dict[str, str]):
        self.dispatch = {k: get_action(v) for k, v in actions.items()}

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            label = ent.label_

            action = self.dispatch.get(label)

            if action:
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
