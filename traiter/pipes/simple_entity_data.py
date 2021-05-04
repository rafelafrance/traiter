"""Actions for enriching matches.

This is most often used after creating entities from phrase patterns.
"""

from typing import Optional

from spacy.language import Language

from traiter.pipes.entity_data import EntityData

SIMPLE_ENTITY_DATA = 'traiter.simple_entity_data.v1'

StrDict = dict[str, str]


@Language.factory(SIMPLE_ENTITY_DATA)
class SimpleEntityData(EntityData):
    """Save the text (lower) in the entity data and cache the label."""

    def __init__(self, nlp: Language, name: str, replace: Optional[StrDict] = None):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.replace = replace if replace else {}

    def __call__(self, doc):
        for ent in doc.ents:
            if label := ent.label_:
                ent._.cached_label = label
                lower = ent.text.lower()
                lower = self.replace.get(lower, lower) if self.replace else lower
                ent._.data[label] = lower
                for token in ent:
                    token._.cached_label = label
        return doc
