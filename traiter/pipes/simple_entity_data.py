"""Actions for enriching matches.

This is most often used after creating entities from phrase patterns.
It may also be used on rule patterns that are very early in the pipeline.
"""

from typing import Optional

from spacy.language import Language

from ..pipe_util import add_spacy_extensions

SIMPLE_ENTITY_DATA = 'simple_entity_data'

add_spacy_extensions()


@Language.factory(SIMPLE_ENTITY_DATA)
def simple_entity_data(
        nlp: Language, name: str, replace: Optional[dict[str, str]] = None):
    """Set update term text."""
    return SimpleEntityData(nlp, name, replace)


class SimpleEntityData:
    """Save the text (lower) in the entity data and cache the label."""

    def __init__(self, nlp, name, replace):
        self.nlp = nlp
        self.name = name
        self.replace = replace

    def __call__(self, doc):
        for ent in doc.ents:
            if label := ent.label_:
                ent._.cached_label = label
                lower = ent.text.lower()
                lower = self.replace.get(lower, lower) if self.replace else lower
                ent._.data[label] = lower
        return doc
