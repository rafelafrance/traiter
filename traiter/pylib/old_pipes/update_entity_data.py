"""Update entity data without creating new entities.

It performs matches and runs functions on those matches. The "after_match" functions
perform the actual updates.
"""
from typing import Any

from spacy import registry
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.util import filter_spans

from ..actions import RejectMatch
from .entity_data import EntityData

UPDATE_ENTITY_DATA = "traiter_update_entity_data_v1"


@Language.factory(UPDATE_ENTITY_DATA)
class UpdateEntityData(EntityData):
    """Perform actions to update user defined fields etc. for all entities."""

    def __init__(self, nlp: Language, name: str, patterns: list[dict]):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.dispatch = {
            p["label"]: registry.misc.get(on)
            for p in patterns
            if (on := p.get("on_match"))
        }

        self.matcher = Matcher(nlp.vocab)
        for matcher in patterns:
            label = matcher["label"]
            self.matcher.add(label, matcher["patterns"], greedy="LONGEST")

    def __call__(self, doc: Doc) -> Doc:
        entities = []
        seen: set[Any] = set()

        matches = self.matcher(doc, as_spans=True)
        matches = filter_spans(matches)

        for ent in matches:
            if action := self.dispatch.get(ent.label_):
                try:
                    action(ent)
                except RejectMatch:
                    continue

            for sub_ent in ent.ents:
                label = sub_ent.label_
                sub_ent, label = self.relabel_entity(sub_ent, label)
                sub_ent._.data["trait"] = label
                entities.append(sub_ent)
                seen.update(range(sub_ent.start, sub_ent.end))

        for ent in doc.ents:
            if ent.start not in seen and ent.end - 1 not in seen:
                entities.append(ent)

        doc.ents = sorted(entities, key=lambda s: s.start)
        return doc
