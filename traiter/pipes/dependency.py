"""Add dependency matcher pipe to the pipeline."""

from array import array
from collections import defaultdict
from typing import Union

import spacy
from spacy.language import Language
from spacy.matcher import DependencyMatcher
from spacy.tokens import Span, Token

from traiter.util import as_list, sign

DEPENDENCY = 'dependency'
NEAREST_ANCHOR = 'nearest_anchor.v1'


NEVER = 9999
PENALTY = {
    ',': 2,
    ';': 5,
    '.': NEVER,
}


def add_extensions():
    """Add extensions for spans and tokens used by entity linker pipes."""
    if not Span.has_extension('links'):
        Span.set_extension('links', default=defaultdict(list))
        Token.set_extension('links', default=defaultdict(list))


@Language.factory(DEPENDENCY)
class Dependency:
    """Matchers that walk the parse tree of a sentence or doc."""

    def __init__(self, nlp: Language, name: str, patterns: Union[dict, list[dict]]):
        self.nlp = nlp
        self.name = name
        self.matcher = DependencyMatcher(nlp.vocab)
        patterns = as_list(patterns)
        self.dispatch = self.build_dispatch_table(patterns)
        self.build_matchers(patterns)
        add_extensions()

    def build_matchers(self, patterns):
        """Setup matchers."""
        for matcher in patterns:
            label = matcher['label']
            self.matcher.add(label, matcher['patterns'])

    def build_dispatch_table(self, patterns):
        """Setup after match actions."""
        dispatch = {}
        for matcher in patterns:
            label = matcher['label']
            label = self.nlp.vocab.strings[label]
            if on_match := matcher.get('on_match'):
                func = spacy.registry.misc.get(on_match['func'])
                dispatch[label] = (func, on_match.get('kwargs', {}))
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
            nearest = [n for n in nearest if n[0][0] < NEVER]
            if nearest:
                nearest = sorted(nearest)[0][1]
                doc.ents[e]._.data[anchor] = doc.ents[nearest]._.data[anchor]
                nearest = doc.ents[nearest]
                doc.ents[e]._.links[f'{anchor}_link'].append(
                    (nearest.start_char, nearest.end_char))


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
