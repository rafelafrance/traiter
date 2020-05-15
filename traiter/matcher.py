"""Common logic for parsing trait notations."""

import sys
from collections import defaultdict

from spacy.matcher import Matcher, PhraseMatcher

from .nlp import NLP
from .pattern import CODES, Type


class Parser:
    """Shared parser logic."""

    def __init__(self, name='', catalog=None):
        self.name = name
        self.catalog = catalog  # The pattern catalog
        self.matchers = []      # Compiled spacy matchers
        self.patterns = defaultdict(dict)   # All patterns grouped by type
        self._built = False

    def get_patterns(self, type_=None):
        """Get patterns by type."""
        if type_:
            return self.patterns[type_].values()
        return [p for v in self.patterns.values() for p in v.values()]

    def add_pattern(self, pattern):
        """Get patterns by type."""
        self.patterns[pattern.type][pattern.name] = pattern

    def build(self):
        """Build the matchers and regular expressions."""
        self.catalog.expand_groupers()
        self.get_implicit_patterns()
        self.build_producers()
        self.build_phrase_matchers()
        self.build_regex_matchers()
        self._built = True

    def get_implicit_patterns(self):
        """Get patterns from catalog if needed but were not added directly."""
        active = {p.name for p in self.get_patterns()}

        for type_ in (Type.GROUPER, Type.PRODUCER):
            for parser in self.get_patterns(type_):
                for word in parser.get_word_set():
                    if word not in active:
                        if pat := self.catalog[word]:
                            self.add_pattern(self.catalog[word])

    def build_producers(self):
        """Create and compile regex out of the producers."""
        groupers = {g.name: g for g in self.get_patterns(Type.GROUPER)}
        for producer in self.get_patterns(Type.PRODUCER):
            producer.build_producer(groupers)

    def build_phrase_matchers(self):
        """Add phrase matcher to the term matchers."""
        if not self.patterns[Type.PHRASE]:
            return

        attrs = defaultdict(list)
        for pattern in self.get_patterns(Type.PHRASE):
            attrs[pattern.attr].append(pattern)

        for attr, patterns in attrs.items():
            matcher = PhraseMatcher(NLP.vocab, attr=attr)
            self.matchers.append(matcher)
            for phrase in patterns:
                phrases = phrase.build_phrase()
                matcher.add(phrase.name, phrases, on_match=self.enrich_tokens)

    def build_regex_matchers(self):
        """Add a regex matcher to the term matchers."""
        if not self.patterns[Type.REGEXP]:
            return
        matcher = Matcher(NLP.vocab)
        self.matchers.append(matcher)
        for regexp in self.get_patterns(Type.REGEXP):
            regexps = regexp.build_regexp()
            matcher.add(regexp.name, regexps, on_match=self.enrich_tokens)

    def use(self, name):
        """Use a pattern from the catalog."""
        self._built = False
        if pattern := self.catalog[name]:
            self.add_pattern(pattern)
        else:
            print(f'Error "{name}" is not in the catalog.', file=sys.stderr)

    def phrase(self, name, attr, terms):
        """Setup a phrase matcher for scanning with spacy."""
        self._built = False
        pattern = self.catalog.phrase(name, attr, terms)
        self.add_pattern(pattern)

    def regexp(self, name, pattern):
        """Setup a regex matcher for scanning with spacy."""
        self._built = False
        pattern = self.catalog.regexp(name, pattern)
        self.add_pattern(pattern)

    def grouper(self, name, pattern):
        """Setup a grouper pattern for parsing with regex."""
        pattern = self.catalog.grouper(name, pattern)
        self.add_pattern(pattern)

    def capture(self, name, pattern):
        """Setup a capture grouper pattern for parsing with regex."""
        pattern = self.catalog.capture(name, pattern)
        self.add_pattern(pattern)

    def producer(self, action, pattern, name=''):
        """Setup a producer regex for parsing with regex."""
        self._built = False
        pattern = self.catalog.producer(action, pattern, name)
        self.add_pattern(pattern)

    def scan(self, text):
        """Find all terms in the text and return the resulting doc.

        There may be more than one matcher for the terms. Gather the results
        for each one and combine them. Then retokenize the doc to handle terms
        that span multiple tokens.
        """
        if not self._built:
            self.build()

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
        doc = self.scan(text)

        # for token in doc:
        #     print(f'{token._.term} {token}')

        # Because we elide over some tokens we need an easy way to map them
        token_map = [t.i for t in doc if t._.code]

        encoded = [t._.code for t in doc if t._.code]
        encoded = ''.join(encoded)

        enriched_matches = []
        for producer in self.get_patterns(Type.PRODUCER):
            for match in producer.compiled.finditer(encoded):
                start, end = match.span()
                enriched_matches.append((producer.action, start, end, match))

        enriched_matches = self.leftmost_longest(enriched_matches)

        all_traits = []
        for enriched_match in enriched_matches:
            action, _, _, match = enriched_match

            traits = action(doc, match, token_map)

            if not traits:
                continue

            all_traits += traits if isinstance(traits, list) else [traits]

        return all_traits

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
