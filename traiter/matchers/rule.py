"""Rule matchers for the pipeline.

Matchers are a list of dicts.
The dict key is the step name.
The dict contains these fields:
    1) The label for the match.
    2) The function to execute when there is a match.
    3) A list of part of speech (POS) to label any match.
    4) A list of spacy patterns. Each pattern is its own list.
"""

from typing import Callable, Dict, List
from warnings import warn

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span

from .base import Base


class Rule(Base):
    """Rule matchers for the pipeline."""

    # We sometimes want to process the same trait name with different actions.
    # This is a tiebreaker for trait names. For instance, we may want to process
    # sizes like "10 m long" differently from "10-15 m long" even though they're
    # both size traits.
    count: int = 0

    def __init__(self, nlp: Language, rules: List[Dict], step: str):
        super().__init__(nlp, step)

        self.matcher = Matcher(nlp.vocab)

        # Action to take on a matched trait. It's trait_name -> action
        self.actions: Dict[str, Callable] = {}

        # Set the part of speech (pos) for the match
        self.pos: Dict[str, List] = {}

        self.build_matcher(rules)

    def build_matcher(self, rules):
        """Build the matcher."""
        for rule in rules:
            Rule.count += 1
            label = f"{rule['label']}.{Rule.count}"
            patterns = rule['patterns']
            self.matcher.add(label, patterns)

            if on_match := rule.get('on_match'):
                self.actions[label] = on_match

            if pos := rule.get('pos'):
                self.pos[label] = pos.split() if isinstance(pos, str) else pos

    def __call__(self, doc: Doc) -> Doc:
        """Find all term in the text and return the resulting doc."""
        spans = self.get_spans(doc)

        with doc.retokenize() as retokenizer:
            for span in spans:
                label = span.label_
                action = self.actions.get(label)
                data = action(span) if action else {}

                if data is None:
                    continue

                pos = self.get_pos(span, label)
                label = label.split('.')[0]
                label = data['_label'] if data.get('_label') else label

                attrs = {'ENT_TYPE': label, 'ENT_IOB': 3, 'POS': pos,
                         '_': {'data': data, 'step': self.step}}

                retokenizer.merge(span, attrs=attrs)

        # self.debug(doc)

        return doc

    def get_pos(self, span: Span, label: str) -> str:
        """Get the part of speech (POS) for a span."""
        pos = self.pos.get(label)
        return span.root.pos_ if (not pos or span.root.pos_ in pos) else pos[0]

    @classmethod
    def add_pipe(cls, nlp: Language, matchers: List[Dict], step: str, **kwargs) -> None:
        """Build rule matchers that recognize traits."""
        kwargs = {'before': 'parser'} if not kwargs else kwargs
        rules = []
        for matcher in matchers:
            rules += matcher.get(step, [])

        if not rules:
            warn(f'Did not find rules for "{step}".')

        matcher = cls(nlp, rules, step)
        nlp.add_pipe(matcher, name=step, **kwargs)
