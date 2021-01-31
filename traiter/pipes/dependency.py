"""Add dependency matcher pipe to the pipeline."""

from array import array
from collections import defaultdict
from typing import Dict, List, Optional

import spacy
from spacy.language import Language
from spacy.matcher import DependencyMatcher

from traiter.util import sign

DEPENDENCY = 'dependency'
NEAREST_LINKER = 'nearest_linker.v1'


@Language.factory(DEPENDENCY, default_config={'after_match': {}})
def dependency(
        nlp: Language,
        name: str,
        patterns: List[List[Dict]],
        after_match: Optional[Dict]
):
    """Build a dependency pipe."""
    return Dependency(nlp, patterns, after_match)


class Dependency:
    """Matchers that walk the parse tree of a sentence or doc."""

    def __init__(self, nlp, patterns, after_match):
        self.nlp = nlp
        self.matcher = DependencyMatcher(nlp.vocab)
        self.after_match = {}
        self.build_matchers(patterns)
        self.build_after_match(after_match)

    def build_matchers(self, patterns):
        """Setup matchers."""
        for pattern_set in patterns:
            for pattern in pattern_set:
                label = pattern['label']
                on_match = pattern.get('on_match')
                on_match = spacy.registry.misc.get(on_match) if on_match else None
                self.matcher.add(label, pattern['patterns'], on_match=on_match)

    def build_after_match(self, after_match):
        """Setup after match actions."""
        for label, values in after_match.items():
            label = self.nlp.vocab.strings[label]
            func = spacy.registry.misc.get(values['func'])
            kwargs = values.get('kwargs', {})
            self.after_match[label] = (func, kwargs)

    def __call__(self, doc):
        matches = self.matcher(doc)

        if not self.after_match:
            return doc

        matches_by_id = defaultdict(list)
        for match in matches:
            matches_by_id[match[0]].append(match)

        for match_id, match_list in matches_by_id.items():
            if post := self.after_match.get(match_id):
                post[0](doc, match_list, **post[1])

        return doc

    @staticmethod
    def after_match_args(*matchers):
        """Build arguments for the post matcher function."""
        after_match = {}
        for matcher in matchers:
            for pattern_set in matcher:
                if post := pattern_set['after_match']:
                    after_match[pattern_set['label']] = post
        return after_match


@spacy.registry.misc(NEAREST_LINKER)
def nearest_linker(doc, matches, **kwargs):
    """Link traits to the root trait trait.

    This uses a simple algorithm for linking traits.
        1) Create a set of matched entities from matches of tokens.
        2) Find all entities
        2) Link entities to closest root entity.
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
