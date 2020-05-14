"""Common logic for parsing trait notations."""

import sys

from spacy.matcher import Matcher, PhraseMatcher

from .nlp import NLP
from .pattern import CODES, Type


class Parser:
    """Shared parser logic."""

    def __init__(self, name='', catalog=None):
        self.name = name
        self.catalog = catalog      # A catalog of all possible rules
        self.active_terms = set()   # AWhat's being used from the catalog
        self.matchers = []          # Compiled spacy matchers
        self.producers = {}         # Compiled producers
        self.replacers = {}

    def build(self):
        """Build the matchers and regular expressions."""
        self.catalog.expand_groupers()
        self.catalog.complete_active_terms(self)
        self.build_producers()
        self.build_phrase_matchers()
        self.build_regex_matchers()

    def complete_active_terms(self, matcher):
        """Find terms that are used but haven't been directly set."""
        for parser in self.catalog.active(matcher, Type.PRODUCER):
            words = parser.get_word_set()
            matcher.active_terms |= {w for w in words if self.catalog.has(w)}

        for parser in self.catalog.active(matcher, Type.GROUPER):
            words = parser.get_word_set()
            matcher.active_terms |= {w for w in words if self.catalog.has(w)}

    def build_producers(self):
        """Create and compile regex out of the producers."""
        groupers = self.catalog.active(Type.GROUPER)
        groupers = {g.name: g for g in groupers}

        producers = self.catalog.active(Type.PRODUCER)
        for producer in producers:
            self.producers[producer.name] = producer.build_producer(groupers)

    def build_phrase_matchers(self):
        """Add phrase matcher to the term matchers."""
        if not (phrases := self.catalog.active(Type.PHRASE)):
            return
        matcher = PhraseMatcher(NLP.vocab)
        self.matchers.append(matcher)
        for phrase in phrases:
            patterns = phrase.build_phrase()
            matcher.add(phrase.name, patterns, on_match=self.enrich_tokens)

    def build_regex_matchers(self):
        """Add a regex matcher to the term matchers."""
        if not (regexps := self.catalog.active(Type.REGEXP)):
            return
        matcher = Matcher(NLP.vocab)
        self.matchers.append(matcher)
        for regexp in regexps:
            patterns = regexp.build_regexp()
            matcher.add(regexp.name, patterns, on_match=self.enrich_tokens)

    def use(self, name):
        """Use a pattern from the catalog."""
        if self.catalog.has(name):
            self.active_terms.add(name)
            return
        print(f'Error "{name}" is not in the catalog.', file=sys.stderr)

    def phrase(self, name, match_on, terms):
        """Setup a phrase mather for scanning with spacy."""
        self.catalog.phrase(name, match_on, terms)
        self.active_terms.add(name)

    def regexp(self, name, pattern):
        """Setup a phrase mather for scanning with spacy."""
        self.catalog.regexp(name, pattern)
        self.active_terms.add(name)

    def grouper(self, name, pattern):
        """Setup a phrase mather for scanning with spacy."""
        self.catalog.grouper(name, pattern)
        self.active_terms.add(name)

    def producer(self, action, pattern, name=''):
        """Setup a phrase mather for scanning with spacy."""
        pattern = self.catalog.producer(action, pattern, name)
        self.active_terms.add(pattern.name)

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
            token._.code = CODES[label]

    def find_terms(self, text):
        """Find all terms in the text and return the resulting doc.

        There may be more than one matcher for the terms. Gather the results
        for each one and combine them. Then retokenize the doc to handle terms
        that span multiple tokens.
        """
        doc = NLP(text)

        matches = []

        for matcher in self.matchers:
            matches += matcher(doc)

        matches = self.leftmost_longest(matches)

        with doc.retokenize() as retokenizer:
            for match_id, start, end in matches:
                retokenizer.merge(doc[start:end])

        return doc

    def parse(self, text):
        """Parse the traits."""
        doc = self.find_terms(text)

        # Because we elide over some tokens we need an easy way to map them
        token_map = [t.i for t in doc if t._.code]

        encoded = [t._.code for t in doc if t._.code]
        encoded = ''.join(encoded)

        enriched_matches = []
        for name, producer in self.producers.items():
            for match in producer.compiled.finditer(encoded):
                start, end = match.span()
                enriched_matches.append((producer.action, start, end, match))

        enriched_matches = self.leftmost_longest(enriched_matches)

        all_traits = []
        for enriched_match in enriched_matches:
            action, _, _, match = enriched_match

            traits = action(self, doc, match, token_map)

            if not traits:
                continue

            all_traits += traits if isinstance(traits, list) else [traits]

            return all_traits
