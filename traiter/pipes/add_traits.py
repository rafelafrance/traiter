"""Combine matches to make a trait."""
from typing import Any

from spacy import registry
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.tokens import Span
from spacy.util import filter_spans

from traiter.actions import RejectMatch
from traiter.pipes.extensions import add_extensions

ADD_TRAITS = "traiter.add_traits.v1"


@Language.factory(ADD_TRAITS)
class AddTraits:
    """Perform actions to fill user defined fields etc. for all entities."""

    def __init__(self, nlp: Language, name: str, patterns: list[dict]):
        add_extensions()

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

    @staticmethod
    def relabel_entity(ent, old_label):
        """Relabel an entity.

        We cannot change a label on a span so we have to make a new one.
        """
        label = old_label

        if new_label := ent._.new_label:
            label = new_label
            span = Span(ent.doc, ent.start, ent.end, label=new_label)
            span._.data = ent._.data
            span._.new_label = ""
            ent = span
            if (move := span._.data.get(old_label)) is not None:
                span._.data[label] = move
                del span._.data[old_label]

        return ent, label
