"""This is just a place to park common matcher functions."""

from typing import Union

from spacy.language import Language
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Doc, Span
from spacy.util import filter_spans

MatcherType = Union[None, PhraseMatcher, Matcher]


class Base:
    """The base matcher object."""

    def __init__(self, nlp: Language, step: str) -> None:
        self.nlp = nlp
        self.step = step
        self.matcher: MatcherType = None

    def debug(self, doc: Doc) -> None:
        """Print debug messages."""
        print('-' * 80)
        print(self.step)
        for token in doc:
            print(f'{token.ent_type_:<15} {token.pos_:<6} {token}')
        print()

    def get_spans(self, doc):
        """Get spans for the matches so that they can be retokenized."""
        matches = self.matcher(doc)
        spans = [Span(doc, s, e, label=i) for i, s, e in matches]
        return filter_spans(spans)
