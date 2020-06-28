"""Common logic for parsing trait notations."""

from collections import defaultdict

from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span
from spacy.util import filter_spans

from .spacy_nlp import spacy_nlp


class TraitMatcher:
    """Shared parser logic."""

    def __init__(self, nlp=None):
        self.nlp = nlp if nlp else spacy_nlp()
        self.matchers = defaultdict(list)  # Patterns to match at each step
        self.actions = {}  # Action to take on a matched trait

    def add_terms(self, terms, step='terms'):
        """Add phrase matchers.

        Each term is a dict with at least these three fields:
            1) attribute: what spacy token field are we matching (ex. LOWER)
            2) label: what is the term's hypernym (ex. color)
            3) pattern: the phrase being matched (ex. gray-blue)
        """
        by_attr = defaultdict(list)

        for pattern in [t for t in terms]:
            by_attr[pattern['attr']].append(pattern)

        for attr, patterns in by_attr.items():
            matcher = PhraseMatcher(self.nlp.vocab, attr=attr)
            self.matchers[step].append(matcher)

            by_label = defaultdict(list)
            for term in terms:
                by_label[term['label']].append(term)

            for label, term_list in by_label.items():
                phrases = [self.nlp.make_doc(t['pattern']) for t in term_list]
                matcher.add(label, phrases)

    def add_patterns(self, rules, step):
        """Build matchers that recognize traits and labels."""
        if not rules:
            return
        matcher = Matcher(self.nlp.vocab)
        self.matchers[step].append(matcher)
        for rule in rules:
            label = rule['label']
            patterns = rule['patterns']
            matcher.add(label, patterns)
            if on_match := rule.get('on_match'):
                self.actions[label] = on_match

    def scan(self, doc, matchers, step):
        """Find all terms in the text and return the resulting doc.
        There may be more than one matcher for the terms. Gather the results
        for each one and combine them. Then retokenize the doc to handle terms
        that span multiple tokens.
        """
        matches = []

        for matcher in matchers:
            matches += matcher(doc)

        spans = [Span(doc, s, e, label=self.nlp.vocab.strings[i])
                 for i, s, e in matches]
        spans = filter_spans(spans)

        with doc.retokenize() as retokenizer:
            for span in spans:
                label = span.label_
                action = self.actions.get(label)
                data = action(span) if action else {}
                if data.get('_retokenize', True):
                    label = data['_relabel'] if data.get('_relabel') else label
                    attrs = {'_': {'label': label, 'data': data, 'step': step}}
                    retokenizer.merge(span, attrs=attrs)

        return doc

    def parse(self, text):
        """Parse the traits."""
        doc = self.nlp(text)

        for step, matchers in self.matchers.items():
            doc = self.scan(doc, self.matchers[step], step=step)

        return doc
