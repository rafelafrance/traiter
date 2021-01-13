"""Custom pipeline component to convert tokens into entities."""

from typing import Optional, Set

from spacy.language import Language
from spacy.tokens import Doc, Span


class ToEntities:  # pylint: disable=too-few-public-methods
    """Custom pipeline component to convert tokens into entities."""

    def __init__(
            self,
            entities2keep: Optional[Set] = None,
            token2entity: Optional[Set] = None
    ) -> None:
        self.entities2keep = entities2keep if entities2keep else set()
        self.token2entity = token2entity if token2entity else set()

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

            if label := token.ent_type_:
                if token._.step not in self.token2entity:
                    continue

                span = Span(doc, token.i, token.i + 1, label=label)

                span._.data = token._.data
                span._.step = token._.step

                span._.data['trait'] = label
                span._.data['start'] = span.start_char
                span._.data['end'] = span.end_char

                new_ents.append(span)

        doc.ents = tuple(new_ents)
        return doc

    @staticmethod
    def add_pipe(
            nlp: Language,
            entities2keep: Optional[Set] = None,
            token2entity: Optional[Set] = None,
            **kwargs
    ) -> None:
        """Add entities converter to the pipeline."""
        kwargs = {'before': 'parser'} if not kwargs else kwargs
        pipe = ToEntities(entities2keep, token2entity)
        nlp.add_pipe(pipe, **kwargs)
