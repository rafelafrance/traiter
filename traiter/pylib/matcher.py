"""Common logic for parsing trait notations."""

from collections import defaultdict
from typing import Callable, DefaultDict, Dict, List, Optional, Union

from spacy.language import Language
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Doc, Span
from spacy.util import filter_spans

from traiter.pylib.util import TERM_STEP

MatcherDict = DefaultDict[str, List[Union[Matcher, PhraseMatcher]]]


class SpacyMatcher:
    """Shared parser logic."""

    def __init__(self, nlp: Optional[Language] = None) -> None:
        self.nlp: Optional[Language] = nlp

        # Patterns to match at each step
        self.matchers: MatcherDict = defaultdict(list)

        # Action to take on a matched trait. So it's trait_name -> action
        self.actions: Dict[str, Callable] = {}

        # We sometimes want to process the same trait name with different actions.
        # This is a tiebreaker for trait names. For instance, we may want to process
        # sizes like "10 m long" differently from "10-15 m long" even though they're
        # both size traits.
        self.count: int = 0

    def add_terms(
            self,
            terms: Dict,
            step: str = TERM_STEP,  # Step name
            on_match: Optional[Callable] = None
    ) -> None:
        """Add phrase matchers.

        Each term is a dict with at least these three fields:
            1) attr: what spacy token field are we matching (ex. LOWER)
            2) label: what is the term's hypernym (ex. color)
            3) pattern: the phrase being matched (ex. gray-blue)
        """
        # Spacy requires that we separate phrase matchers by match attribute
        attrs = {p['attr'] for p in terms}
        for attr in attrs:
            matcher = PhraseMatcher(self.nlp.vocab, attr=attr)
            self.matchers[step].append(matcher)

            by_label = defaultdict(list)
            for term in terms:
                if term['attr'] == attr:
                    by_label[term['label']].append(term)

            for label, term_list in by_label.items():
                phrases = [self.nlp.make_doc(t['pattern']) for t in term_list]
                matcher.add(label, phrases)
                if on_match:
                    self.actions[label] = on_match

    def add_patterns(self, matchers: List[Dict], step: str) -> Optional[List[Dict]]:
        """Build matchers that recognize traits and labels."""
        rules = self.step_rules(matchers, step)
        if not rules:
            return None

        matcher = Matcher(self.nlp.vocab)
        self.matchers[step].append(matcher)
        for rule in rules:
            self.count += 1
            label = f"{rule['label']}.{self.count}"
            patterns = rule['patterns']
            matcher.add(label, patterns)
            if on_match := rule.get('on_match'):
                self.actions[label] = on_match

        return rules

    @staticmethod
    def step_rules(matchers: List[Dict], step: str) -> List[Dict]:
        """Get all patterns for a step."""
        rules = []
        for matcher in matchers:
            rules += matcher.get(step, [])
        return rules

    def retokenize(self, doc: Doc, step: str) -> Doc:
        """Find all term in the text and return the resulting doc."""
        spans = self.find_matches(doc, step)

        with doc.retokenize() as retokenizer:
            for span in spans:
                label = span.label_
                action = self.actions.get(label)
                data = action(span) if action else {}
                if data.get('_forget'):
                    continue
                label = label.split('.')[0]
                label = data['_label'] if data.get('_label') else label
                attrs = {'ENT_TYPE': label, 'ENT_IOB': 3,
                         '_': {'data': data, 'step': step}}
                retokenizer.merge(span, attrs=attrs)

        return doc

    def find_matches(self, doc: Doc, step: str) -> List[Span]:
        """Find matches in the doc."""
        matchers = self.matchers[step]

        matches = []
        for matcher in matchers:
            matches += matcher(doc)
        spans = [Span(doc, s, e, label=i) for i, s, e in matches]
        spans = filter_spans(spans)
        return spans

    def __call__(self, doc: Doc) -> Doc:
        """Parse the doc in steps, building up a full parse in steps."""
        for step, _ in self.matchers.items():  # Preserve order
            doc = self.retokenize(doc, step)

            # print('-' * 80)
            # print(step)
            # for token in doc:
            #     print(f'{token.ent_type_:<15} {token.pos_:<6} {token}')
            # print()

        return doc
