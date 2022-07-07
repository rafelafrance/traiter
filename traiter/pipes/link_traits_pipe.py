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
        parents: list[str],
        children: list[str],
        patterns: list[dict],
        weights: dict[str, int] = None,
    ):
        pipe_util.add_extensions()

        self.nlp = nlp
        self.name = name
        self.parents = parents
        self.children = children
        self.weights = {k.lower(): v for k, v in weights.items()} if weights else {}
        self.matcher = self.build_matcher(nlp, patterns)

    @staticmethod
    def build_matcher(nlp, patterns):
        matcher = Matcher(nlp.vocab)
        for pat in patterns:
            matcher.add(pat["label"], pat["patterns"])
        return matcher

    def __call__(self, doc: Doc) -> Doc:
        matches = self.matcher(doc, as_spans=True)
        matches = self.filter_matches(doc, matches)

        for span in matches:
            if len(span) <= 1:
                continue

            # Get the parent and child locations
            if span[0].ent_type_ in self.parents:
                t_idx, p_idx = span.end - 1, span.start
            else:
                t_idx, p_idx = span.start, span.end - 1

            # Get the parent's trait
            parent = self.get_ent_from_token(doc, doc[p_idx].i)
            parent_trait = parent._.data["trait"]

            # Update the child entity and token
            ent = self.get_ent_from_token(doc, doc[t_idx].i)
            ent._.data[parent_trait] = doc[p_idx]._.data[parent_trait]
            doc[t_idx]._.data[parent_trait] = ent._.data[parent_trait]

        return doc

    @staticmethod
    def get_ent_from_token(doc, token_idx):
        return next(e for e in doc.ents if e.start <= token_idx < e.end)

    def filter_matches(self, doc, matches):
        # Find the index of the child token -- it's at one end or the other
        idx = [
            m.end - 1 if m[0].ent_type_ in self.parents else m.start for m in matches
        ]
        if self.weights:
            distances = self.weighted_distances(doc, matches)
        else:
            distances = [m.end - m.start for m in matches]
        matches = zip(idx, distances, matches)
        matches = sorted(matches)
        grouped = groupby(matches, key=lambda m: m[0])
        matches = [list(g)[0][2] for _, g in grouped]
        return matches

    def weighted_distances(self, doc, matches):
        distances = []
        for match in matches:
            dist = 0
            for idx in range(match.start, match.end):
                token = doc[idx]
                dist += self.weights.get(token.lower_, 1)
            distances.append(dist)
        return distances
