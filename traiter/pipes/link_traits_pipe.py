from collections import defaultdict
from itertools import product

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc

from traiter import util
from traiter.pipes import pipe_util

LINK_TRAITS = "traiter_link_traits_v1"

NO_LIMIT = 999_999


# ####################################################################################
class LinkMatch:
    def __init__(self, span, weights, doc, parents, reverse_weights):
        self.span = span
        self.doc = doc
        self.weights = weights
        self.parents = parents
        self.child_idx, self.parent_idx = self.get_indices()
        self.child_ent = self.get_ent_from_token(self.child_idx)
        self.parent_ent = self.get_ent_from_token(self.parent_idx)
        self.child_trait = self.child_ent._.data["trait"]
        self.parent_trait = self.parent_ent._.data["trait"]
        self.reverse_weights = reverse_weights
        self.distance = self.weighted_distance()

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
        weights = self.weights
        if self.parent_idx > self.child_idx:
            weights = self.reverse_weights
        return sum(
            weights.get(self.doc[i].lower_, 1)
            for i in range(self.span.start, self.span.end)
        )


# ####################################################################################
class LinkCount:
    def __init__(self, differ: list[str], max_count: int):
        self.differ = differ
        self.max_count = max_count
        self.seen: dict[tuple, int] = defaultdict(int)

    def all_values(self, ent):
        return [v for d in self.differ if (v := util.as_list(ent._.data.get(d, [])))]

    def seen_too_much(self, ent):
        """Check if we've seen this link type (parent to trait) too many times."""
        return any(
            self.seen[k] >= self.max_count for k in product(*self.all_values(ent))
        )

    def update_seen(self, ent):
        """Update the already seen values for each field."""
        for key in product(*self.all_values(ent)):
            self.seen[key] += 1


# ####################################################################################
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
        reverse_weights: dict[str, int] = None,  # Weights for scoring backwards
        max_links: int = NO_LIMIT,  # Max times to link to a parent trait
        differ: list[str] = None,
    ):
        pipe_util.add_extensions()

        self.nlp = nlp
        self.name = name
        self.parents = parents
        self.parent_set = set(parents)
        self.children = children
        self.weights = {k.lower(): v for k, v in weights.items()} if weights else {}
        self.reverse_weights = (
            {k.lower(): v for k, v in reverse_weights.items()}
            if reverse_weights
            else self.weights
        )
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
        matches = [
            LinkMatch(m, self.weights, doc, self.parents, self.reverse_weights)
            for m in matches
        ]
        matches = sorted(matches)

        parent_link_count = defaultdict(lambda: LinkCount(self.differ, self.max_links))

        for match in matches:
            if len(match) <= 1:
                continue

            # See if this trait is already linked
            if set(match.child_ent._.data.keys()) & self.parent_set:
                continue

            # See if the parent link limit is exceeded
            link_count = parent_link_count[match.parent_idx, match.child_trait]
            if link_count.seen_too_much(match.child_ent):
                continue
            link_count.update_seen(match.child_ent)

            # Update the child entity
            if match.parent_trait in match.parent_ent._.data:
                parent_trait = match.parent_ent._.data[match.parent_trait]
                match.child_ent._.data[match.parent_trait] = parent_trait

        return doc
