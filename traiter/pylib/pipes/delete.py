from spacy.language import Language
from spacy.tokens import Doc

DELETE_TRAITS = "traiter_delete_traits_v3"


@Language.factory(DELETE_TRAITS)
class DeleteTraits:
    """Delete partial or unwanted traits.

    Traits are built up in layers and sometimes a partial traits in lower layers are
    not used in an upper layer. This will cause noisy output, so delete them.
    Note: This deletes the entity/span not its tokens.

    delete: Is a list of traits that get deleted.
    """

    def __init__(self, nlp: Language, name: str, delete: list[str] = None):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.delete = delete if delete else []

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent._.delete:
                self.clear_tokens(ent)
                continue

            if ent.label_ in self.delete:
                self.clear_tokens(ent)
                continue

            entities.append(ent)

        doc.set_ents(entities)
        return doc

    @staticmethod
    def clear_tokens(ent):
        for token in ent:
            token._.term = ""
