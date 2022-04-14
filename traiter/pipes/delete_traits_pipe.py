"""Remove noise partial traits from the doc."""
from spacy import registry
from spacy.language import Language
from spacy.tokens import Doc

DELETE_TRAITS = "traiter.delete_traits.v1"


@Language.factory(DELETE_TRAITS)
class DeleteTraits:
    """Delete partial or unwanted traits.

    Traits are built up in layers and sometimes a partial trait in a lower layer is
    not used in an upper layer. This will cause noisy output, so delete them.
    Note: This deletes the entity/span not its tokens.
    """

    def __init__(
        self, nlp: Language, name: str, delete: list[str] = None, delete_when: str = ""
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.delete = delete if delete else []
        if delete_when:
            self.delete_when = registry.misc.get(delete_when)
        else:
            self.delete_when = lambda _: False

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ in self.delete or self.delete_when(ent):
                continue
            entities.append(ent)

        doc.set_ents(entities)
        return doc
