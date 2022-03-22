"""Remove noise entities from the docLINK_NEAREST = 'traiter.link_nearest.v1'
."""

from spacy.language import Language
from spacy.tokens import Doc

from traiter.pipes.pipes import CLEANUP


@Language.factory(CLEANUP)
class Cleanup:
    """Save current token label so it can be used after it is replaced."""

    def __init__(self, nlp: Language, name: str, forget: list[str]):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.forget = forget

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ not in self.forget:
                entities.append(ent)

        doc.ents = entities
        return doc
