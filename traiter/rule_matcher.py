"""Rule matchers for the pipeline.

Matchers are a list of dicts.
The dict key is the step name.
The dict contains these fields:
    1) The label for the match.
    2) The function to execute when there is a match.
    3) A list of spacy patterns. Each pattern is its own list.
"""

from typing import Callable, Dict, List
from warnings import warn

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span
from spacy.util import filter_spans


class RuleMatcher:
    """Rule matchers for the pipeline."""

    # We sometimes want to process the same trait name with different actions.
    # This is a tiebreaker for trait names. For instance, we may want to process
    # sizes like "10 m long" differently from "10-15 m long" even though they're
    # both size traits.
    count: int = 0

    def __init__(self, nlp: Language, rules: List[Dict], step: str):
        self.matcher = Matcher(nlp.vocab)
        self.step = step

        # Action to take on a matched trait. So it's trait_name -> action
        self.actions: Dict[str, Callable] = {}

        # Build the matcher
        for rule in rules:
            RuleMatcher.count += 1
            label = f"{rule['label']}.{RuleMatcher.count}"
            patterns = rule['patterns']
            self.matcher.add(label, patterns)
            if on_match := rule.get('on_match'):
                self.actions[label] = on_match

    def __call__(self, doc: Doc) -> Doc:
        """Find all term in the text and return the resulting doc."""
        matches = self.matcher(doc)

        spans = [Span(doc, s, e, label=i) for i, s, e in matches]
        spans = filter_spans(spans)

        with doc.retokenize() as retokenizer:
            for span in spans:
                label = span.label_
                action = self.actions.get(label)
                data = action(span) if action else {}

                if data is None:
                    continue

                label = label.split('.')[0]
                label = data['_label'] if data.get('_label') else label

                attrs = {'ENT_TYPE': label, 'ENT_IOB': 3,
                         '_': {'data': data, 'step': self.step}}

                retokenizer.merge(span, attrs=attrs)

        # print('-' * 80)
        # print(self.step)
        # for token in doc:
        #     print(f'{token.ent_type_:<15} {token._.step:<8} {token.pos_:<6} {token}')
        # print()

        return doc

    @staticmethod
    def add_pipe(nlp: Language, matchers: List[Dict], step: str, **kwargs) -> None:
        """Build rule matchers that recognize traits."""
        rules = []
        for matcher in matchers:
            rules += matcher.get(step, [])

        if not rules:
            warn(f'Did not find rules for "{step}".')

        matcher = RuleMatcher(nlp, rules, step)
        nlp.add_pipe(matcher, name=step, **kwargs)
