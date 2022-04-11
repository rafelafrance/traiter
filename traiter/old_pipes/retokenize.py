"""Retokenize entities and carry 'ent._.*' data over to the new entities."""
from typing import Any

from spacy.language import Language
from spacy.tokens import Doc

RETOKENIZE = "traiter.retokenize.v1"


@Language.factory(RETOKENIZE)
class Retokenize:
    """Merge entities into a single token also merge the 'ent._.*' data."""

    def __init__(self, nlp: Language, name: str):
        super().__init__()
        self.nlp = nlp
        self.name = name

    def __call__(self, doc: Doc) -> Doc:
        with doc.retokenize() as retokenizer:
            for ent in doc.ents:
                data: dict[str, Any] = {}
                for token in ent:
                    data |= token._.data
                data |= ent._.data
                label = ent.label_
                attrs = {
                    "ENT_TYPE": label,
                    "ENT_IOB": 3,
                    "_": {"data": data, "cached_label": label},
                }
                retokenizer.merge(ent, attrs=attrs)

        return doc
