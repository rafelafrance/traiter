"""Add dependency matcher pipe to the pipeline."""

from array import array
from collections import defaultdict

import spacy
from spacy.language import Language
from spacy.matcher import DependencyMatcher

from traiter.util import sign

DEPENDENCY = 'dependency'
NEAREST_ANCHOR = 'nearest_anchor.v1'


@Language.factory(DEPENDENCY)
def dependency(nlp: Language, name: str, patterns: list[list[dict]]):
    """Build a dependency pipe."""
    return Dependency(nlp, name, patterns)


class Dependency:
    """Matchers that walk the parse tree of a sentence or doc."""

    def __init__(self, nlp, name, patterns):
        self.nlp = nlp
        self.name = name
        self.matcher = DependencyMatcher(nlp.vocab)
        self.dispatch = self.build_dispatch_table(patterns)
        self.build_matchers(patterns)

    def build_matchers(self, patterns):
        """Setup matchers."""
        for pattern_set in patterns:
            for pattern in pattern_set:
                label = pattern['label']
                self.matcher.add(label, pattern['patterns'])

    def build_dispatch_table(self, patterns):
        """Setup after match actions."""
        dispatch = {}
        for matcher in patterns:
            for pattern_set in matcher:
                label = pattern_set['label']
                label = self.nlp.vocab.strings[label]
                if on_match := pattern_set.get('on_match'):
                    if isinstance(on_match, str):
                        func = on_match
                        kwargs = {}
                    else:
                        func = on_match['func']
                        kwargs = on_match.get('kwargs', {})
                    func = spacy.registry.misc.get(func)
                    dispatch[label] = (func, kwargs)
        return dispatch

    def __call__(self, doc):
        matches = self.matcher(doc)

        if not self.dispatch:
            return doc

        matches_by_id = defaultdict(list)
        for match in matches:
            matches_by_id[match[0]].append(match)

        for match_id, match_list in matches_by_id.items():
            if after := self.dispatch.get(match_id):
                after[0](doc, match_list, **after[1])

        return doc


@spacy.registry.misc(NEAREST_ANCHOR)
def nearest_anchor(doc, matches, **kwargs):
    """Link traits to the nearest anchor trait.

    This uses a simple algorithm for linking traits.
        1) Create a set of matched entities from matches of tokens.
        2) Find all entities.
        2) Link entities to closest anchor entity. There are different distance metrics.
    """
    # print(kwargs)
    # print(matches)
    anchor = kwargs.get('anchor')
    exclude = kwargs.get('exclude')

    # The dependency tree is built by a neural net before the linker rules are run.
    # The dependency tree links tokens, not spans/entities to tokens.
    # Therefore a tree arc may point to any token in an entity/span and many arcs
    #       may point to the same entity.
    # We want to add data to the entity not to the tokens.
    # So we need to map tokens in the matches to entities.
    anchor_2_ent = array('i', [-1] * len(doc))
    token_2_ent = array('i', [-1] * len(doc))

    for e, ent in enumerate(doc.ents):
        if ent.label_ == exclude:
            continue
        elif ent.label_ == anchor:
            anchor_2_ent[ent.start:ent.end] = array('i', [e] * len(ent))
        else:
            token_2_ent[ent.start:ent.end] = array('i', [e] * len(ent))

    # From the matches with token indexes get the entity index
    anchor_idx, ent_idx = set(), set()
    for _, token_ids in matches:
        ent_idx |= {e for t in token_ids if (e := token_2_ent[t]) > -1}
        anchor_idx |= {e for t in token_ids if (e := anchor_2_ent[t]) > -1}

    # Find the closest anchor entity to the target entity
    for e in ent_idx:
        if not doc.ents[e]._.data.get(anchor):
            nearest = [(token_penalty(a, e, doc), a) for a in anchor_idx]
            nearest = sorted(nearest)[0][1]
            doc.ents[e]._.data[anchor] = doc.ents[nearest]._.data[anchor]


PENALTY = {
    ',': 2,
    ';': 5,
}


def token_penalty(anchor_i, entity_i, doc):
    """Calculate the token offset from the anchor to the entity, penalize punct."""
    lo, hi = (entity_i, anchor_i) if entity_i < anchor_i else (anchor_i, entity_i)
    lo, hi = doc.ents[lo][-1].i, doc.ents[hi][0].i
    dist = hi - lo
    penalty = sum(PENALTY.get(doc[i].text, 0) for i in range(lo + 1, hi))
    return dist + penalty, sign(anchor_i - entity_i)


def token_distance(anchor_i, entity_i, doc):
    """Calculate token offset from the anchor to the entity."""
    hi, lo = (anchor_i, entity_i) if anchor_i > entity_i else (entity_i, anchor_i)
    dist = doc.ents[hi][0].i - doc.ents[lo][-1].i
    return dist, sign(anchor_i - entity_i)


def entity_distance(anchor_i, entity_i, _):
    """Calculate the distance in token offset from the anchor to the entity."""
    dist = anchor_i - entity_i
    return abs(dist), sign(dist)
