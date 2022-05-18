"""Remove noise partial traits from the doc."""
from typing import Any

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

    delete: Is a list of traits that get deleted. They're all considered to be
        partially formed traits.

    delete_when: Takes the name of a registered function (or a list of function names)
        and deletes the trait if any of them return true. These functions take an
        entity and return a boolean.
    """

    def __init__(
        self,
        nlp: Language,
        name: str,
        delete: list[str] = None,
        delete_when: dict[str, Any] = None,
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.delete = delete if delete else []

        delete_when = delete_when if delete_when else {}
        self.delete_when = {}
        for label, funcs in delete_when.items():
            funcs = funcs if isinstance(funcs, list) else [funcs]
            self.delete_when[label] = [registry.misc.get(f) for f in funcs]

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            label = ent.label_
            if ent._.delete:
                continue
            if label in self.delete:
                continue
            if self.delete_when and any(
                f(ent) for f in self.delete_when.get(label, [])
            ):
                continue
            entities.append(ent)

        doc.set_ents(entities)
        return doc
