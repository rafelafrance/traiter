"""Phrase matchers for terms.

Add a phrase matcher for each match attribute in the term list.
Spacy requires that we separate phrase matchers by match attribute.

Each term is a dict with at least these three fields:
    1) attr: what spacy token field are we matching (ex. LOWER)
    2) label: what is the term's hypernym (ex. color)
    3) pattern: the phrase being matched (ex. gray-blue)
    ** There may be other fields in the dict but this module does not use them.
"""

from collections import defaultdict
from typing import Callable, Dict, List, Optional

from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc

from traiter.util import TERM_STEP
from .base import Base


class Term(Base):
    """Phrase matchers for the pipeline."""

    def __init__(
            self,
            nlp: Language,
            terms: List,
            attr: str = 'lower',
            step: str = TERM_STEP,
            action: Optional[Callable] = None
    ) -> None:
        super().__init__(nlp, step)

        self.matcher = PhraseMatcher(nlp.vocab, attr=attr)
        self.action = action

        # Group terms by label
        by_label = defaultdict(list)
        for term in terms:
            by_label[term['label']].append(term)

        # Add patterns for each label
        for label, term_list in by_label.items():
            phrases = [nlp.make_doc(t['pattern']) for t in term_list]
            self.matcher.add(label, phrases)

    def __call__(self, doc: Doc) -> Doc:
        """Find all term in the text and return the resulting doc."""
        spans = self.get_spans(doc)

        with doc.retokenize() as retokenizer:
            for span in spans:
                label = span.label_
                data = self.action(span) if self.action else {}

                attrs = {'ENT_TYPE': label, 'ENT_IOB': 3,
                         '_': {'data': data, 'step': self.step}}

                retokenizer.merge(span, attrs=attrs)

        # self.debug(doc)

        return doc

    @classmethod
    def add_pipes(
            cls,
            nlp: Language,
            terms: List[Dict],
            step: str = TERM_STEP,
            action: Optional[Callable] = None,
            **kwargs
    ) -> None:
        """Add one terms matcher for each term attribute."""
        by_attr = defaultdict(list)
        for term in terms:
            by_attr[term['attr']].append(term)

        for attr, attr_terms in by_attr.items():
            matcher = cls(nlp, attr_terms, attr=attr, step=step, action=action)
            pipe_name = f'{step}_{attr}'
            nlp.add_pipe(matcher, name=pipe_name, **kwargs)
