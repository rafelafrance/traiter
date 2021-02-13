"""Remove noise entities from the doc."""

from spacy.language import Language
from spacy.tokens import Doc

CLEANUP = 'clean_up'


@Language.factory(CLEANUP)
class Cleanup:
    """Save current token label so it can be used after it is replaced."""

    def __init__(self, nlp: Language, name: str, entities: list[str]):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.entities = entities

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ not in self.entities:
                entities.append(ent)

        doc.ents = entities
        return doc
