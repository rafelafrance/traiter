import json
from pathlib import Path
from typing import Any

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.util import filter_spans
from spacy.util import registry

from traiter.pylib.pipes.reject_match import RejectMatch

ADD_TRAITS = "add_traits"


@Language.factory(ADD_TRAITS)
class AddTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        patterns: dict[str, list[list[dict[str, Any]]]],
        dispatch: dict[str, str] | None = None,
        keep: list[str] | None = None,  # Don't overwrite these entities
        overwrite: list[str] | None = None,  # Only overwrite these entities
        relabel: dict[str, str] | None = None,
    ):
        self.nlp = nlp
        self.name = name
        self.patterns = patterns
        self.dispatch = dispatch
        self.keep = keep if keep else []
        self.overwrite = overwrite if overwrite else []
        self.relabel = relabel if relabel else {}

        self.dispatch_table = self.build_dispatch_table()
        self.matcher = self.build_matcher()

    def build_dispatch_table(self):
        dispatch_table = {}
        if self.dispatch:
            for label, registered in self.dispatch.items():
                if func := registry.misc.get(registered):
                    dispatch_table[label] = func
        return dispatch_table

    def build_matcher(self):
        matcher = Matcher(self.nlp.vocab, validate=True)
        # Don't match too much if we are keeping traits
        greedy = None if self.keep or self.overwrite else "LONGEST"
        for label, patterns in self.patterns.items():
            matcher.add(label, patterns, greedy=greedy)
        return matcher

    def __call__(self, doc: Doc) -> Doc:
        entities = []
        used_tokens: set[Any] = set()

        matches = self.matcher(doc, as_spans=True)

        if self.overwrite:
            self.keep_unflagged_entities(doc, entities, used_tokens)
            matches = self.remove_overlapping_matches(matches, used_tokens)

        if self.keep:
            self.keep_flagged_entities(doc, entities, used_tokens)
            matches = self.remove_overlapping_matches(matches, used_tokens)

        matches = filter_spans(matches)

        for ent in matches:
            label = ent.label_

            ent_tokens = set(range(ent.start, ent.end))
            if ent_tokens & used_tokens:
                continue

            if action := self.dispatch_table.get(label):
                try:
                    action(ent)
                except RejectMatch:
                    continue

            used_tokens |= ent_tokens

            label = self.relabel_entity(ent, label)

            ent._.data["trait"] = label
            ent._.data["start"] = ent.start_char
            ent._.data["end"] = ent.end_char
            entities.append(ent)

        self.add_untouched_entities(doc, entities, used_tokens)

        doc.set_ents(sorted(entities, key=lambda s: s.start))
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
                used_tokens |= ent_tokens
                entities.append(ent)

    def keep_unflagged_entities(self, doc, entities, used_tokens):
        for ent in doc.ents:
            if ent.label_ not in self.overwrite:
                ent_tokens = set(range(ent.start, ent.end))
                used_tokens |= ent_tokens
                entities.append(ent)

    def relabel_entity(self, ent, old_label):
        label = old_label

        new_label = self.relabel.get(old_label)
        new_label = ent._.relabel if ent._.relabel else new_label
        if new_label:
            if new_label not in self.nlp.vocab.strings:
                self.nlp.vocab.strings.add(new_label)
            ent.label = self.nlp.vocab.strings[new_label]
            label = new_label

        return label

    def to_disk(self, path, exclude=tuple()):  # noqa
        path = Path(path)
        if not path.exists():
            path.mkdir()
        data_path = path / "data.json"
        skips = ("nlp", "name", "dispatch_table", "matcher")
        fields = {k: v for k, v in self.__dict__.items() if k not in skips}
        with data_path.open("w", encoding="utf8") as data_file:
            data_file.write(json.dumps(fields))

    def from_disk(self, path, exclude=tuple()):  # noqa
        data_path = Path(path) / "data.json"
        with data_path.open("r", encoding="utf8") as data_file:
            data = json.load(data_file)
            for key in data.keys():
                self.__dict__[key] = data[key]
            self.matcher = self.build_matcher()
            self.dispatch_table = self.build_dispatch_table()
