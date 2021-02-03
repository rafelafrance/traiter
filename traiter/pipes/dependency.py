"""Add dependency matcher pipe to the pipeline."""

from array import array
from collections import defaultdict

import spacy
from spacy.language import Language
from spacy.matcher import DependencyMatcher

from traiter.util import sign

DEPENDENCY = 'dependency'
NEAREST_LINKER = 'nearest_linker.v1'


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


@spacy.registry.misc(NEAREST_LINKER)
def nearest_linker(doc, matches, **kwargs):
    """Link traits to the root trait trait.

    This uses a simple algorithm for linking traits.
        1) Create a set of matched entities from matches of tokens.
        2) Find all entities.
        2) Link entities to closest root entity, favoring entities being downstream
           being downstream of the root entity.
    """
    # print(kwargs)
    # print(matches)
    root = kwargs.get('root')
    exclude = kwargs.get('exclude')

    # The dependency tree is built by a neural net before the linker rules are run.
    # The dependency tree links tokens, not spans/entities to tokens.
    # Therefore a tree arc may point to any token in an entity/span and many arcs
    #       may point to the same entity.
    # We want to add data to the entity not to the tokens.
    # So we need to map tokens in the matches to entities.
    root_2_ent = array('i', [-1] * len(doc))
    token_2_ent = array('i', [-1] * len(doc))

    for i, ent in enumerate(doc.ents):
        if ent.label_ == exclude:
            continue
        elif ent.label_ == root:
            root_2_ent[ent.start:ent.end] = array('i', [i] * len(ent))
        else:
            token_2_ent[ent.start:ent.end] = array('i', [i] * len(ent))

    # From the matches with token indexes get the entity index
    root_indexes, ent_indexes = set(), set()
    for _, token_ids in matches:
        ent_indexes |= {e for t in token_ids if (e := token_2_ent[t]) > -1}
        root_indexes |= {e for t in token_ids if (e := root_2_ent[t]) > -1}

    # Find the closest root entity to the target entity
    for ent_idx in ent_indexes:
        nearest = sorted(root_indexes, key=lambda r: (abs(r - ent_idx), -sign(r)))[0]
        doc.ents[ent_idx]._.data[root] = doc.ents[nearest]._.data[root]
