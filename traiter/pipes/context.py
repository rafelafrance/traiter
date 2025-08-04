"""
Match a trait defined by its surrounding traits without changing the surrounding traits.

The normal trait matcher builds a new trait including all the tokens and subentities
in the match. This pipe allows you to match a trait without snowballing all the other
traits. It is based on traits so you the new trait must be a previous phrase or another
trait match.
"""

from typing import Any

from spacy import util
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span

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
        overwrite: list[str] | None = None,
    ):
        self.nlp = nlp
        self.name = name
        self.patterns = patterns
        self.dispatch = dispatch
        self.overwrite = overwrite

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

    def __call__new(self, doc: Doc) -> Doc:
        matches = self.matcher(doc, as_spans=True)

        matches = util.filter_spans(matches)
        if not matches:
            return doc

        entities = doc.ents

        for match in matches:
            label = match.label_

            traits = []
            if action := self.dispatch_table.get(label):
                try:
                    traits = action(match)
                    traits = traits if isinstance(traits, list) else [traits]
                except RejectMatch:
                    return doc

            for trait in traits:
                span = doc.char_span(trait.start, trait.end, label=trait._trait)
                span._.trait = trait
                entities = [
                    e for e in entities if (e.start < span.start or e.start >= span.end)
                ]
                entities.append(span)

        entities = sorted(entities, key=lambda e: e.start)
        doc.set_ents(entities, default="unmodified")

        return doc

    def __call__(self, doc: Doc) -> Doc:
        matches = self.matcher(doc, as_spans=True)

        matches = util.filter_spans(matches)
        if not matches:
            return doc

        entities = doc.ents

        for ent in matches:
            label = ent.label_

            trait = None
            if action := self.dispatch_table.get(label):
                try:
                    trait = action(ent)
                except RejectMatch:
                    return doc

            start, end = 1e10, -1
            for sub_ent in ent.ents:
                if sub_ent.label_ in self.overwrite:
                    start = min(start, sub_ent.start)
                    end = max(end, sub_ent.end)

            entities = [e for e in entities if (e.start < start or e.start >= end)]

            new_ent = Span(doc=doc, start=start, end=end, label=label)
            trait.start = new_ent.start_char
            trait.end = new_ent.end_char
            trait._text = new_ent.text
            new_ent._.trait = trait

            entities.append(new_ent)

        entities = sorted(entities, key=lambda e: e.start)
        doc.set_ents(entities, default="unmodified")

        return doc
