"""Add dependency matcher pipe to the pipeline."""

import string
from array import array
from collections import defaultdict, namedtuple
from typing import Union

import spacy
from spacy.language import Language
from spacy.matcher import DependencyMatcher
from spacy.tokens import Span, Token

from traiter.pipes.pipes import DEPENDENCY
from traiter.pipes.pipes import LINK_NEAREST
from traiter.util import as_list, sign


DependencyPatterns = Union[dict, list[dict]]


def add_extensions():
    """Add extensions for spans and tokens used by entity linker pipes."""
    if not Span.has_extension('links'):
        Span.set_extension('links', default={})
        Token.set_extension('links', default={})


@Language.factory(DEPENDENCY)
class Dependency:
    """Matchers that walk the parse tree of a sentence or doc."""

    def __init__(self, nlp: Language, name: str, patterns: DependencyPatterns):
        self.nlp = nlp
        self.name = name
        self.matcher = DependencyMatcher(nlp.vocab)
        patterns = as_list(patterns)
        self.dispatch = self.build_dispatch_table(patterns)
        self.build_matchers(patterns)
        add_extensions()

    def build_matchers(self, patterns: DependencyPatterns):
        """Setup matchers."""
        for matcher in patterns:
            label = matcher['label']
            self.matcher.add(label, matcher['patterns'])

    def build_dispatch_table(self, patterns: DependencyPatterns):
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


LinkAnchor = namedtuple('LinkAnchor', 'dist dir_ text')


@spacy.registry.misc(LINK_NEAREST)
def link_nearest(doc, matches, **kwargs):
    """Link traits."""
    anchor = kwargs.get('anchor')
    exclude = kwargs.get('exclude', '')
    dir_bias = kwargs.get('dir_bias', '')
    bias = -1 if dir_bias == 'after' else 1
    entity_matches = tokens2entities(doc, matches)

    # All possible anchors for every entity
    groups = defaultdict(list)
    for token_idx in entity_matches:
        anchor_i = [i for i in token_idx if doc.ents[i].label_ == anchor][0]
        text = doc.ents[anchor_i]._.data[anchor]
        entities = []
        for i in token_idx:
            if doc.ents[i].label_ != anchor and doc.ents[i].label_ != exclude:
                entities.append(i)
        for entity_i in entities:
            dist, dir_ = weighted_distance(anchor_i, entity_i, doc, bias)
            groups[entity_i].append(LinkAnchor(dist, dir_, text))

    # Find the closest (weighted) anchor to the entity
    for entity_i, link_anchors in groups.items():
        nearest = sorted(link_anchors, key=lambda a: (a.dist, a.dir_))[0]
        entity = doc.ents[entity_i]
        entity._.data[anchor] = nearest.text


NEVER = 9999
PENALTY = {
    ',': 2,
    ';': 5,
    '.': NEVER,
}


def weighted_distance(anchor_i, entity_i, doc, bias):
    """Calculate the token offset from the anchor to the entity, penalize punct.

    Also indicate if the anchor is before or after the entity.
    """
    lo, hi = (entity_i, anchor_i) if entity_i < anchor_i else (anchor_i, entity_i)
    lo, hi = doc.ents[lo][-1].i, doc.ents[hi][0].i
    dist = hi - lo
    first, last = doc[lo+1].idx + len(doc[lo+1]), doc[hi].idx
    seg = doc.text[first-1:last+1]
    if seg and seg[0] == '.' and seg[-1] in string.ascii_uppercase:
        dist += NEVER
    for i in range(lo + 1, hi):
        dist += PENALTY.get(doc[i].text, 0)
    # dist += sum(PENALTY.get(doc[i].text, 0) for i in range(lo + 1, hi))
    dir_ = sign(anchor_i - entity_i) * bias
    return dist, dir_


def tokens2entities(doc, matches):
    """Convert token indices in the matches to entity indices.

    The dependency tree is built by a neural net before running the linker rules.
    The dependency tree links tokens (not spans/entities) to tokens. Therefore a
    tree arc may point to any token in an entity/span and many arcs may point to
    the same entity. We want to add data to the entity not to the tokens. So we
    need to map tokens in the matches to entities. This function turns match token
    indices into entity indices.
    """
    token2ent = array('i', [-1] * len(doc))

    # This creates an array of tokens indices and the entity indices they map to
    for e, ent in enumerate(doc.ents):
        token2ent[ent.start:ent.end] = array('i', [e] * len(ent))

    # Map the matched tokens to entities, remove duplicates and remove non-entities
    mapped = {tuple(e for i in t_idx if (e := token2ent[i]) >= 0)
              for _, t_idx in matches}

    return sorted(mapped)
