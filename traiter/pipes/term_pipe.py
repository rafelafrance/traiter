"""Use spacy's phrase matcher to create terms."""
from collections import defaultdict
from typing import Any
from typing import Optional

from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc
from spacy.util import filter_spans

TERM_PIPE = "traiter.term_pipe.v1"
PHRASE_PIPE = "traiter.phrase_pipe.v1"


@Language.factory(TERM_PIPE)
class TermPipe:
    """Add a phrase matcher for each attribute (attr) int terms."""

    def __init__(
        self,
        nlp: Language,
        name: str,
        terms: list[dict],
        replace: Optional[dict[str, str]] = None,
        overwrite: bool = False,
    ):
        self.pipes = []
        for attr, term_list in split_by_attr(terms).items():
            name = f"{name}_{attr}"
            self.pipes.append(
                PhrasePipe(nlp, name, term_list, attr, replace, overwrite)
            )

    def __call__(self, doc: Doc) -> Doc:
        for pipe in self.pipes:
            doc = pipe(doc)
        return doc


@Language.factory(PHRASE_PIPE)
class PhrasePipe:
    """Add a phrase matcher."""

    def __init__(
        self,
        nlp: Language,
        name: str,
        terms: list[dict],
        attr: str = "lower",
        replace: Optional[dict[str, str]] = None,
        overwrite: bool = False,
    ):
        self.nlp = nlp
        self.name = name
        self.overwrite = overwrite
        self.replace = replace if replace else {}

        self.matcher = PhraseMatcher(self.nlp.vocab, attr=attr.upper())

        by_label = defaultdict(list)
        for term in terms:
            by_label[term["label"]].append(term)

        for label, term_list in by_label.items():
            phrases = [self.nlp.make_doc(t["pattern"]) for t in term_list]
            self.matcher.add(label, phrases)

    def __call__(self, doc: Doc) -> Doc:
        entities = []
        used_tokens: set[Any] = set()

        matches = self.matcher(doc, as_spans=True)
        matches = filter_spans(matches)

        if not self.overwrite:
            for ent in doc.ents:
                entities.append(ent)
                used_tokens.update(range(ent.start, ent.end))

        for ent in matches:
            label = ent.label_
            texts = []

            ent_tokens = set(range(ent.start, ent.end))

            if not self.overwrite:
                if ent_tokens & used_tokens:
                    continue

            for token in ent:
                token._.cached_label = label
                text = self.replace.get(token.lower_, token.text)
                token._.data[label] = text
                texts.append(text)
                texts.append(token.whitespace_)

            used_tokens.update(ent_tokens)

            ent._.data[label] = "".join(texts).strip()
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


def split_by_attr(terms: list[dict]) -> dict[str, list[dict]]:
    """Categorize terms by their attr so that we can make matcher per attr.

    The returned dictionary's key is the attr and the value is a list of terms with
    that attr.
    """
    by_attr = defaultdict(list)
    for term in terms:
        by_attr[term["attr"]].append(term)
    return by_attr
