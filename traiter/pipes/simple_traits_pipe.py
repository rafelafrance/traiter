"""Actions for enriching matches.

This is most often used after creating entities from phrase patterns. All we're doing
is adding "data" to already existing entities to turn them into traits.
"""
from typing import Optional

from spacy.language import Language

from traiter.pipes.pipe_util import add_extensions

SIMPLE_TRAITS = "traiter.simple_traits.v2"

StrDict = Optional[dict[str, str]]
StrList = Optional[list[str]]


@Language.factory(SIMPLE_TRAITS)
class SimpleTraits:
    """Save the text in the entity data and cache the label."""

    def __init__(
        self, nlp: Language, name: str, replace: StrDict = None, update: StrList = None
    ):
        add_extensions()

        self.nlp = nlp
        self.name = name
        self.update = update if update else []
        self.replace = replace if replace else {}

    def __call__(self, doc):
        for ent in doc.ents:
            label = ent.label_
            if label and (not self.update or label in self.update):
                ent._.cached_label = label
                texts = []
                for token in ent:
                    token._.cached_label = label
                    text = self.replace.get(token.lower_, token.text)
                    token._.data[label] = text
                    texts.append(text)
                    texts.append(token.whitespace_)
                ent._.data[label] = "".join(texts).strip()
                ent._.data["trait"] = label
                ent._.data["start"] = ent.start_char
                ent._.data["end"] = ent.end_char
        return doc
