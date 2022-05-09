"""Perform actions to fill user defined fields for traits."""
from collections import defaultdict
from itertools import groupby

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc

from traiter.pipes import pipe_util

LINK_TRAITS = "traiter.link_traits.v1"


@Language.factory(LINK_TRAITS)
class LinkTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        parent: str,
        children: list[str],
        patterns: list[dict],
        times: int = 0,
    ):
        pipe_util.add_extensions()

        self.nlp = nlp
        self.name = name
        self.parent = parent
        self.children = children
        self.times = times

        self.matcher = self.build_matcher(nlp, patterns)

    @staticmethod
    def build_matcher(nlp, patterns):
        matcher = Matcher(nlp.vocab)
        for pat in patterns:
            matcher.add(pat["label"], pat["patterns"])
        return matcher

    def __call__(self, doc: Doc) -> Doc:
        matches = self.matcher(doc, as_spans=True)
        matches = self.filter_matches(matches)
        times = defaultdict(int)

        for span in matches:
            if len(span) > 1:
                if span[0].ent_type_ == self.parent:
                    t_idx, p_idx = span.end - 1, span.start
                else:
                    t_idx, p_idx = span.start, span.end - 1

                times[p_idx] += 1
                if self.times and times[p_idx] > self.times:
                    continue

                ent = self.get_ent_from_token(doc, doc[t_idx].i)
                ent._.data[self.parent] = doc[p_idx]._.data[self.parent]
                doc[t_idx]._.data[self.parent] = ent._.data[self.parent]

        return doc

    @staticmethod
    def get_ent_from_token(doc, token_idx):
        return [e for e in doc.ents if e.start <= token_idx < e.end][0]

    def filter_matches(self, matches):
        idx = [m.end - 1 if m[0].ent_type_ == self.parent else m.start for m in matches]
        dists = [m.end - m.start for m in matches]
        matches = zip(idx, dists, matches)
        matches = sorted(matches)
        grouped = groupby(matches, key=lambda m: m[0])
        matches = [list(m)[0][2] for _, m in grouped]
        return matches
