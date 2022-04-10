"""Actions for enriching entities with new data."""
from typing import Any

from spacy import registry
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.util import filter_spans

from traiter.actions import RejectMatch
from traiter.pipes.entity_data import EntityData

ADD_ENTITIES = "traiter.add_entities.v1"


@Language.factory(ADD_ENTITIES)
class AddEntities(EntityData):
    """Perform actions to fill user defined fields etc. for all entities."""

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

            if action := self.dispatch.get(label):
                try:
                    action(ent)
                except RejectMatch:
                    continue

                # Save the old label
                for token in ent:
                    token._.cached_label = token.ent_type_

                ent, label = self.relabel_entity(ent, label)

            seen.update(range(ent.start, ent.end))

            ent._.data["trait"] = label
            ent._.data["start"] = ent.start_char
            ent._.data["end"] = ent.end_char
            entities.append(ent)

        for ent in doc.ents:
            if ent.start not in seen and ent.end - 1 not in seen:
                entities.append(ent)

        doc.ents = sorted(entities, key=lambda s: s.start)
        return doc
