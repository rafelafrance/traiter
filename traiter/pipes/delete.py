from spacy.language import Language
from spacy.tokens import Doc

from .pipe_util import clear_tokens

DELETE_COUNT = 0

DELETE_TRAITS = "delete_traits"


def pipe(nlp: Language, delete: list[str]) -> None:
    global DELETE_COUNT
    DELETE_COUNT += 1
    config = {"delete": delete}
    nlp.add_pipe(DELETE_TRAITS, name=f"{DELETE_TRAITS}_{DELETE_COUNT}", config=config)


@Language.factory(DELETE_TRAITS)
class DeleteTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        delete: list[str],  # List of traits to delete
    ) -> None:
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.delete = delete if delete else []

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ in self.delete:
                clear_tokens(ent)
                continue

            entities.append(ent)

        doc.ents = entities
        return doc
