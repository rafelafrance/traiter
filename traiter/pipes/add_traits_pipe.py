from typing import Any
from typing import Optional

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

    def __init__(
        self,
        nlp: Language,
        name: str,
        patterns: list[dict],
        keep: Optional[list[str]] = None,  # Don't overwrite these entities
    ):
        pipe_util.add_extensions()

        self.nlp = nlp
        self.name = name
        self.keep = keep if keep else []

        self.dispatch = self.build_dispatch_table(patterns)
        self.matcher = self.build_matcher(keep, nlp, patterns)

    @staticmethod
    def build_dispatch_table(patterns):
        # Get the on_match registered functions for the patterns
        return {
            p["label"]: registry.misc.get(on)
            for p in patterns
            if (on := p.get("on_match"))
        }

    @staticmethod
    def build_matcher(keep, nlp, patterns):
        matcher = Matcher(nlp.vocab)
        greedy = None if keep else "LONGEST"  # Don't match too much if keeping traits
        for pat in patterns:
            label = pat["label"]
            matcher.add(label, pat["patterns"], greedy=greedy)
        return matcher

    def __call__(self, doc: Doc) -> Doc:
        entities = []
        used_tokens: set[Any] = set()

        matches = self.matcher(doc, as_spans=True)

        if self.keep:
            self.keep_flagged_entities(doc, entities, used_tokens)
            matches = self.remove_overlapping_matches(matches, used_tokens)

        matches = filter_spans(matches)

        for ent in matches:
            label = ent.label_

            ent_tokens = set(range(ent.start, ent.end))
            if ent_tokens & used_tokens:
                continue

            if action := self.dispatch.get(label):
                try:
                    action(ent)
                except RejectMatch:
                    continue

                self.cache_old_labels(ent)

                label = self.relabel_entity(ent, label)

            used_tokens.update(range(ent.start, ent.end))

            ent._.data["trait"] = label
            ent._.data["start"] = ent.start_char
            ent._.data["end"] = ent.end_char
            entities.append(ent)

        self.add_untouched_entities(doc, entities, used_tokens)

        doc.set_ents(sorted(entities, key=lambda s: s.start))
        return doc

    @staticmethod
    def cache_old_labels(ent):
        for token in ent:
            token._.cached_label = token.ent_type_

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
            match_tokens = set(range(match.start, match.end))
            if match_tokens & used_tokens:
                continue
            filtered_matches.append(match)
        matches = filtered_matches
        return matches

    def keep_flagged_entities(self, doc, entities, used_tokens):
        for ent in doc.ents:
            if ent.label_ in self.keep:
                ent_tokens = set(range(ent.start, ent.end))
                used_tokens.update(ent_tokens)
                entities.append(ent)

    def relabel_entity(self, ent, old_label):
        """Relabel an entity."""
        label = old_label

        if new_label := ent._.new_label:
            if new_label not in self.nlp.vocab.strings:
                self.nlp.vocab.strings.add(new_label)
            ent.label = self.nlp.vocab.strings[new_label]
            label = new_label

        return label
