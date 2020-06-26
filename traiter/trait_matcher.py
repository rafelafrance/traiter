"""Common logic for parsing trait notations."""

from collections import defaultdict

from spacy.matcher import Matcher, PhraseMatcher

from .spacy_nlp import spacy_nlp


class TraitMatcher:
    """Shared parser logic."""

    def __init__(self, nlp=None):
        self.nlp = nlp if nlp else spacy_nlp()
        self.matchers = defaultdict(list)  # Patterns to match at each step
        self.actions = {}  # Action to take on a matched trait

    def add_terms(self, terms, step='terms'):
        """Add phrase matcher to the term matchers."""
        by_attr = defaultdict(list)

        for pattern in [t for t in terms if t['attr'].upper() != 'REGEX']:
            by_attr[pattern['attr']].append(pattern)

        for attr, patterns in by_attr.items():
            self.add_phrase_matcher(attr, patterns, step)

        patterns = [t for t in terms if t['attr'].upper() == 'REGEX']
        if patterns:
            self.add_regex_matcher(patterns, step)

    def add_phrase_matcher(self, attr, terms, step):
        """Add a phrase matcher to the term matchers."""
        matcher = PhraseMatcher(self.nlp.vocab, attr=attr)
        self.matchers[step].append(matcher)

        by_label = defaultdict(list)
        for term in terms:
            by_label[term['label']].append(term)

        for label, term_list in by_label.items():
            phrases = [self.nlp.make_doc(t['pattern']) for t in term_list]
            matcher.add(label, phrases)

    def add_regex_matcher(self, terms, step):
        """Add a regex matcher to the term matchers."""
        matcher = Matcher(self.nlp.vocab)
        self.matchers[step].append(matcher)
        for term in terms:
            regexp = [[{'TEXT': {'REGEX': term['pattern']}}]]
            matcher.add(term['label'], regexp)

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

        matches = self.leftmost_longest(matches)

        with doc.retokenize() as retokenizer:
            for match_id, start, end in matches:
                span = doc[start:end]
                label = self.nlp.vocab.strings[match_id]
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
            # from pprint import pp
            # print(step)
            # pp([f'{t._.label:<15} {t._.data} {t.text}' for t in doc])
            # print()

        return doc

    @staticmethod
    def leftmost_longest(matches):
        """
        Return the longest of any overlapping matches, removing others.

        Matches: array of tuples: [(match_id, start, end), ...]
        """
        if not matches:
            return []
        first, *rest = sorted(matches, key=lambda m: (m[1], -m[2]))
        cleaned = [first]
        for match in rest:
            if match[1] >= cleaned[-1][2]:
                cleaned.append(match)
        return cleaned
