"""Update entity data without creating new entities.

It performs matches and runs functions on those matches. The "after_match" functions
perform does the actual merging of data.
"""
from typing import Any

from spacy import registry
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.util import filter_spans

from traiter.actions import RejectMatch
from traiter.old_pipes.entity_data import EntityData

MERGE_ENTITY_DATA = "traiter.merge_entity_data.v1"


@Language.factory(MERGE_ENTITY_DATA)
class MergeEntityData(EntityData):
    """Perform actions to merge user defined fields etc. for all entities."""

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
            label = ent.label_

            if action := self.dispatch.get(ent.label_):
                try:
                    action(ent)
                except RejectMatch:
                    continue

                ent, label = self.relabel_entity(ent, label)

            seen.update(range(ent.start, ent.end))

            for sub_ent in ent.ents:
                if sub_ent._.merge:
                    ent._.data |= sub_ent._.data

            ent._.data["trait"] = label
            ent._.data["start"] = ent.start_char
            ent._.data["end"] = ent.end_char
            entities.append(ent)

        for ent in doc.ents:
            if ent.start not in seen and ent.end - 1 not in seen:
                entities.append(ent)

        doc.ents = sorted(entities, key=lambda s: s.start)
        return doc
