from typing import Any

from spacy import util
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc

from traiter.pipes.reject_match import RejectMatch

CONTEXT_TRAITS = "context_traits"


@Language.factory(CONTEXT_TRAITS)
class ContextTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        patterns: dict[str, list[list[dict[str, Any]]]],
        dispatch: dict[str, str] | None = None,
        context: list[str] | None = None,  # The trait is surrounded by these entities
    ):
        self.nlp = nlp
        self.name = name
        self.patterns = patterns
        self.dispatch = dispatch
        self.context = context if context else []

        self.dispatch_table = self.build_dispatch_table()
        self.matcher = self.build_matcher()

    def build_dispatch_table(self):
        dispatch_table = {}
        if self.dispatch:
            for label, registered in self.dispatch.items():
                if func := util.registry.misc.get(registered):
                    dispatch_table[label] = func
        return dispatch_table

    def build_matcher(self):
        matcher = Matcher(self.nlp.vocab)
        for label, patterns in self.patterns.items():
            matcher.add(label, patterns, greedy="LONGEST")
        return matcher

    def __call__(self, doc: Doc) -> Doc:
        matches = self.matcher(doc, as_spans=True)

        entities, used_tokens = self.filter_entities(doc)

        matches = self.remove_overlapping_matches(matches, used_tokens)
        matches = util.filter_spans(matches)

        for ent in matches:
            label = ent.label_

            ent_tokens = set(range(ent.start, ent.end))
            if ent_tokens & used_tokens:
                continue

            trait = None
            if action := self.dispatch_table.get(label):
                try:
                    trait = action(ent)
                except RejectMatch:
                    continue

            used_tokens |= ent_tokens

            ent._.trait = trait
            entities.append(ent)

        self.add_untouched_entities(doc, entities, used_tokens)

        doc.set_ents(sorted(entities, key=lambda e: e.start))
        return doc

    @staticmethod
    def add_untouched_entities(doc, entities, used_tokens):
        """Add entities that do not overlap with any of the matches."""
        for ent in doc.ents:
            ent_tokens = set(range(ent.start, ent.end))
            if not ent_tokens & used_tokens:
                entities.append(ent)

    @staticmethod
    def remove_overlapping_matches(matches, used_tokens):
        """Remove any matches that overlap with an entity we kept."""
        filtered_matches = []
        for match in matches:
            ent_tokens = set(range(match.start, match.end))
            if ent_tokens & used_tokens:
                continue
            filtered_matches.append(match)
        return filtered_matches

    def filter_entities(self, doc):
        used_tokens: set[Any] = set()
        entities = []
        for ent in doc.ents:
            if ent.label_ in self.overwrite or ent.label_ not in self.keep:
                continue
            if ent.label_ in self.keep:
                ent_tokens = set(range(ent.start, ent.end))
                used_tokens |= ent_tokens
                entities.append(ent)
        return entities, used_tokens
