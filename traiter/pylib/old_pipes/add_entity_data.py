"""Actions for enriching entities with new data."""
from spacy import registry
from spacy.language import Language
from spacy.tokens import Doc

from ..actions import RejectMatch
from .entity_data import DispatchTable
from .entity_data import EntityData

ADD_ENTITY_DATA = "traiter_add_entity_data_v1"


@Language.factory(ADD_ENTITY_DATA)
class AddEntityData(EntityData):
    """Perform actions to fill user defined fields etc. for all entities."""

    def __init__(self, nlp: Language, name: str, dispatch: DispatchTable):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.dispatch = {k: registry.misc.get(v) for k, v in dispatch.items()}

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            label = ent.label_

            if action := self.dispatch.get(label):
                try:
                    action(ent)
                except RejectMatch:
                    continue

                ent, label = self.relabel_entity(ent, label)

            ent._.data["trait"] = label
            ent._.data["start"] = ent.start_char
            ent._.data["end"] = ent.end_char
            entities.append(ent)

        doc.ents = entities
        return doc