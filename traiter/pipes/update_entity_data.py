"""Update entity data without creating new entities.

It performs matches and then runs functions on those matches.
"""

from typing import Callable, Dict, List

import spacy
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc

from traiter.entity_data_util import add_extensions

UPDATE_ENTITY_DATA = 'update_entity_data'

add_extensions()


@Language.factory(UPDATE_ENTITY_DATA)
def update_entity_data(nlp: Language, name: str, patterns: List[List[Dict]]):
    """Create a entity data dispatch table."""
    return UpdateEntityData(nlp, patterns)


class UpdateEntityData:
    """Perform actions to update user defined fields etc. for all entities."""

    def __init__(self, nlp, patterns: List[List[Dict]]):
        self.nlp = nlp
        self.matcher = Matcher(nlp.vocab)
        self.build_matchers(patterns)

    def build_matchers(self, patterns):
        """Setup matchers."""
        for pattern_set in patterns:
            for pattern in pattern_set:
                label = pattern['label']
                on_match = pattern.get('on_match')
                on_match = spacy.registry.misc.get(on_match) if on_match else None
                self.matcher.add(
                    label, pattern['patterns'], on_match=on_match, greedy='LONGEST')

    def __call__(self, doc: Doc) -> Doc:
        self.matcher(doc, as_spans=True)
        return doc
