"""Remove noise entities from the doc."""
from spacy import registry
from spacy.language import Language
from spacy.tokens import Doc

CLEANUP = "traiter_clean_up_v1"


@Language.factory(CLEANUP)
class Cleanup:
    """Save current token label, so it can be used after it is replaced."""

    def __init__(
        self, nlp: Language, name: str, forget: list[str] = None, forget_when: str = ""
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.forget = forget if forget else []
        if forget_when:
            self.forget_when = registry.misc.get(forget_when)
        else:
            self.forget_when = lambda _: False

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ in self.forget or self.forget_when(ent):
                continue
            entities.append(ent)

        doc.ents = entities
        return doc
