from spacy.language import Language
from spacy.tokens import Doc

from .pipe_util import clear_tokens

CLEANUP_TRAITS = "cleanup_traits"


@Language.factory(CLEANUP_TRAITS)
class CleanupTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        keep: list[str] | None = None,  # List of trait labels to keep
    ) -> None:
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.keep = keep if keep else []

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ not in self.keep:
                clear_tokens(ent)
                continue

            entities.append(ent)

        doc.ents = entities
        return doc
