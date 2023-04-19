import json
from collections import defaultdict
from pathlib import Path

from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc
from spacy.util import filter_spans


PHRASE_PIPE = "phrase_pipe"


@Language.factory(PHRASE_PIPE)
class PhrasePipe:
    def __init__(
        self,
        nlp: Language,
        name: str,
        patterns: list[dict],
        attr: str = "lower",
        replace: dict[str, str] | None = None,
    ):
        self.nlp = nlp
        self.name = name
        self.patterns = patterns
        self.replace = replace if replace else {}
        self.attr = attr

        self.matcher = self.build_matcher()

    def build_matcher(self):
        matcher = PhraseMatcher(self.nlp.vocab, attr=self.attr.upper())

        by_label = defaultdict(list)
        for term in self.patterns:
            by_label[term["label"]].append(term)

        for label, term_list in by_label.items():
            phrases = [self.nlp.make_doc(t["pattern"]) for t in term_list]
            matcher.add(label, phrases)

        return matcher

    def __call__(self, doc: Doc) -> Doc:
        entities = []
        used_tokens = set()

        matches = self.matcher(doc, as_spans=True)
        matches = filter_spans(matches)

        for ent in doc.ents:
            entities.append(ent)
            used_tokens.update(range(ent.start, ent.end))

        for ent in matches:
            label = ent.label_
            texts = []

            ent_tokens = set(range(ent.start, ent.end))
            if ent_tokens & used_tokens:
                continue

            for token in ent:
                token._.term = label
                text = self.replace.get(token.lower_, token.text)
                token._.data[label] = text
                texts.append(text)

            used_tokens |= ent_tokens

            text = " ".join(texts)
            ent._.data[label] = self.replace.get(text, text)
            ent._.data["trait"] = label
            ent._.data["start"] = ent.start_char
            ent._.data["end"] = ent.end_char
            entities.append(ent)

        doc.set_ents(sorted(entities, key=lambda s: s.start))

        return doc

    def to_disk(self, path, exclude=tuple()):  # noqa
        path = Path(path)
        if not path.exists():
            path.mkdir()
        data_path = path / "data.json"
        skips = ("nlp", "name", "matcher")
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
