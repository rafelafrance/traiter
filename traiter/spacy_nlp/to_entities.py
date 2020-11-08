"""Custom pipeline component to convert tokens into entities."""

# pylint: disable=too-few-public-methods
from typing import Optional, Set

from spacy.tokens import Doc, Span


class ToEntities:
    """Custom pipeline component to convert tokens into entities."""

    entities2keep = set()
    token2entity = set()

    def __init__(
        self, entities2keep: Optional[Set] = None, token2entity: Optional[Set] = None
    ) -> None:
        if entities2keep:
            self.entities2keep = entities2keep
        if token2entity:
            self.token2entity = token2entity

    def __call__(self, doc: Doc) -> Doc:
        """Convert trait tokens into entities."""
        new_ents = []

        keep = set()  # Keep these entities

        for ent in doc.ents:
            if ent.label_ in self.entities2keep:
                new_ents.append(ent)
                keep |= set(range(ent.start, ent.end))

        for token in doc:
            if token.i in keep:
                continue

            if ent_type_ := token.ent_type_:
                if token._.step not in self.token2entity:
                    continue
                if token._.data.get('_skip'):
                    continue

                span = Span(doc, token.i, token.i + 1, label=ent_type_)

                span._.data = token._.data
                span._.step = token._.step

                new_ents.append(span)

        doc.ents = tuple(new_ents)
        return doc
