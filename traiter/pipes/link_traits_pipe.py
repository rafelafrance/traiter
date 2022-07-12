from collections import defaultdict

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc

from traiter.pipes import pipe_util

LINK_TRAITS = "traiter.link_traits.v1"

NO_LIMIT = 999_999


class LinkMatch:
    def __init__(self, span, weights, doc, parents):
        self.span = span
        self.doc = doc
        self.weights = weights
        self.parents = parents
        self.distance = self.weighted_distance()
        self.child_idx, self.parent_idx = self.get_indices()
        self.child_ent = self.get_ent_from_token(self.child_idx)
        self.parent_ent = self.get_ent_from_token(self.parent_idx)
        self.child_trait = self.child_ent._.data["trait"]
        self.parent_trait = self.parent_ent._.data["trait"]

    def __lt__(self, other):
        return self.distance < other.distance

    def __len__(self):
        return len(self.span)

    def get_ent_from_token(self, token_idx):
        return next(e for e in self.doc.ents if e.start <= token_idx < e.end)

    def get_indices(self):
        child_idx, parent_idx = self.span.start, self.span.end - 1
        if self.span[0].ent_type_ in self.parents:
            child_idx, parent_idx = parent_idx, child_idx
        return child_idx, parent_idx

    def weighted_distance(self):
        return sum(
            self.weights.get(self.doc[i].lower_, 1)
            for i in range(self.span.start, self.span.end)
        )


@Language.factory(LINK_TRAITS)
class LinkTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        parents: list[str],
        children: list[str],
        patterns: list[dict],
        weights: dict[str, int] = None,  # Token weights for scoring distances
        max_links: int = NO_LIMIT,  # Max times to link to a parent trait
        differ: list[str] = None,
    ):
        pipe_util.add_extensions()

        self.nlp = nlp
        self.name = name
        self.parents = parents
        self.children = children
        self.weights = {k.lower(): v for k, v in weights.items()} if weights else {}
        self.max_links = max_links
        self.differ = differ if differ else []
        self.matcher = self.build_matcher(nlp, patterns)

    @staticmethod
    def build_matcher(nlp, patterns):
        matcher = Matcher(nlp.vocab)
        for pat in patterns:
            matcher.add(pat["label"], pat["patterns"])
        return matcher

    def __call__(self, doc: Doc) -> Doc:
        matches = self.matcher(doc, as_spans=True)
        matches = [LinkMatch(m, self.weights, doc, self.parents) for m in matches]
        matches = sorted(matches)

        parent_link_count = defaultdict(int)
        child_link_count = defaultdict(int)

        for match in matches:
            if len(match) <= 1:
                continue

            # See if the link limit will be exceeded
            key = [match.parent_idx, match.child_trait]
            key += [match.child_ent._.data.get(d, "") for d in self.differ]
            key = tuple(key)
            parent_link_count[key] += 1
            if parent_link_count[key] > self.max_links:
                continue

            # See if this trait is already linked
            key = (match.child_idx, match.parent_trait)
            child_link_count[key] += 1
            if child_link_count[key] > 1:
                continue

            # Update the child entity and token
            if match.parent_trait in match.parent_ent._.data:
                parent_trait = match.parent_ent._.data[match.parent_trait]
                match.child_ent._.data[match.parent_trait] = parent_trait
                doc[match.child_idx]._.data[match.parent_trait] = parent_trait

        return doc
