"""Perform actions to fill user defined fields for traits."""
from typing import Any

from spacy import registry
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.util import filter_spans

from traiter.actions import RejectMatch
from traiter.pipes import pipe_util

ADD_TRAITS = "traiter.add_traits.v1"


@Language.factory(ADD_TRAITS)
class AddTraits:
    """Perform actions to fill user defined fields for traits."""

    def __init__(self, nlp: Language, name: str, patterns: list[dict]):
        pipe_util.add_extensions()

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
        used_tokens: set[Any] = set()

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

                ent, label = pipe_util.relabel_entity(ent, label)

            used_tokens.update(range(ent.start, ent.end))

            ent._.data["trait"] = label
            ent._.data["start"] = ent.start_char
            ent._.data["end"] = ent.end_char
            entities.append(ent)

        for ent in doc.ents:
            ent_tokens = set(range(ent.start, ent.end))
            if not ent_tokens & used_tokens:
                entities.append(ent)

        doc.set_ents(sorted(entities, key=lambda s: s.start))
        return doc
