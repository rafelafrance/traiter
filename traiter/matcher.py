"""Common logic for parsing trait notations."""

from collections import defaultdict

from spacy.matcher import Matcher, PhraseMatcher

from .nlp import NLP


class Parser:
    """Shared parser logic."""

    def __init__(self):
        self.term_matchers = []     # Spacy matchers for terms
        self.trait_matchers = []    # Spacy matchers for traits
        self.actions = {}           # Action to take on a matched trait

    def add_terms(self, terms):
        """Add phrase matcher to the term matchers."""
        by_attr = defaultdict(list)

        for pattern in [t for t in terms if t['attr'].upper() != 'REGEX']:
            by_attr[pattern['attr']].append(pattern)

        for attr, patterns in by_attr.items():
            self.add_phrase_matcher(attr, patterns)

        patterns = [t for t in terms if t['attr'].upper() == 'REGEX']
        if patterns:
            self.add_regex_matcher(patterns)

    def add_phrase_matcher(self, attr, terms):
        """Add a phrase matcher to the term matchers."""
        matcher = PhraseMatcher(NLP.vocab, attr=attr)
        self.term_matchers.append(matcher)

        by_label = defaultdict(list)
        for term in terms:
            by_label[term['label']].append(term)

        for label, term_list in by_label.items():
            phrases = [NLP.make_doc(t['pattern']) for t in term_list]
            matcher.add(label, phrases, on_match=self.enrich_tokens)

    def add_regex_matcher(self, terms):
        """Add a regex matcher to the term matchers."""
        matcher = Matcher(NLP.vocab)
        self.term_matchers.append(matcher)
        for term in terms:
            regexp = [[{'TEXT': {'REGEX': term['pattern']}}]]
            matcher.add(term['label'], regexp, on_match=self.enrich_tokens)

    def add_patterns(self, rules):
        """Build matchers that recognize traits."""
        matcher = Matcher(NLP.vocab)
        self.trait_matchers.append(matcher)
        for label, rule in rules.items():
            patterns = rule['patterns']
            on_match = rule['on_match']
            matcher.add(label, patterns)
            self.actions[label] = on_match

    def scan(self, text):
        """Find all terms in the text and return the resulting doc.
        There may be more than one matcher for the terms. Gather the results
        for each one and combine them. Then retokenize the doc to handle terms
        that span multiple tokens.
        """
        doc = NLP(text)

        matches = []

        for matcher in self.term_matchers:
            matches += matcher(doc)

        matches = self.leftmost_longest(matches)

        with doc.retokenize() as retokenizer:
            for match_id, start, end in matches:
                retokenizer.merge(doc[start:end])

        return doc

    def parse(self, text):
        """Parse the traits."""
        doc = self.scan(text)

        # for token in doc:
        #     print(token._.term, token.text)

        matches = []
        for matcher in self.trait_matchers:
            matches += matcher(doc)

        matches = self.leftmost_longest(matches)

        with doc.retokenize() as retokenizer:
            for match in matches:
                match_id, start, end = match
                span = doc[start:end]
                label = NLP.vocab.strings[match_id]
                data = self.actions[label](span)
                attrs = {'_': {'label': label, 'data': data}}
                retokenizer.merge(span, attrs=attrs)

        # for token in doc:
        #     print(token._.label, token._.data, token.text)

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

    @staticmethod
    def enrich_tokens(_, doc, i, matches):
        """Add data to tokens."""
        match_id, start, end = matches[i]
        label = doc.vocab.strings[match_id]
        for token in doc[start:end]:
            token._.term = label
