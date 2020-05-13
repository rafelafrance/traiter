"""Common logic for parsing trait notations."""

from collections import defaultdict

import regex
from spacy.matcher import Matcher, PhraseMatcher

from .catalog import CODES
from .nlp import NLP
from .util import FLAGS


class Parser:
    """Shared parser logic."""

    # Find tokens in the regex. Look for words that are not part of a group
    # name or a metacharacter. So, "word" not "<word>". Neither "(?P" nor "\b"
    word_re = regex.compile(r"""
        (?<! \(\?P< ) (?<! \(\? ) (?<! [\\] )
        \b (?P<word> [a-z]\w* ) \b """, FLAGS)

    def __init__(self, name='', catalog=None):
        self.name = name
        self.catalog = catalog
        self.matchers = {}
        self.groupers = {}
        self.producers = {}
        self.nlp = NLP

    def grouper(self, name, pattern):
        """Add a grouper to the rules."""
        self.groupers[name] = pattern

    def producer(self, action, pattern):
        """Add a grouper to the rules."""
        name = action.__qualname__
        self.producers[name] = (action, pattern)

    def build(self):
        """Build the matchers and regular expressions."""
        self.build_groupers()
        self.build_producers()
        self.build_spacy_matchers()

    def get_terms(self):
        """Get the terms from the groupers and producers."""

    def build_groupers(self):
        """Create regular expressions out of the groupers."""
        groupers = {}
        for key, value in self.groupers.items():
            if isinstance(value, list):
                value = '|'.join(f'(?:{v})' for v in value)
            value = ' '.join(value.split())
            groupers[key] = f'(?:{value})'
        self.groupers = groupers

    def build_producers(self):
        """Create and compile regex out of the producers."""
        def _replace(match):
            word = match.group('word')
            return f'(?:{CODES[word]})'

        producers = []
        for p_func, p_regex in self.raw_producers:
            for g_name, g_regex in self.groupers.items():
                p_regex = p_regex.replace(g_name, g_regex)
            p_regex = self.word_re.sub(_replace, p_regex)
            p_regex = ' '.join(p_regex.split())
            p_regex = regex.compile(p_regex, FLAGS)
            producers.append([p_func, p_regex])
        self.producers = producers

    def parse(self, text):
        """Parse the traits."""
        raise NotImplementedError

    def build_spacy_matchers(self):
        """Build terms for this matcher."""
        term_types = defaultdict(list)

        for term in self.catalog:
            if term['type'] in self.term_list:
                term_types[(term['match_on'], term['type'])].append(term)

        for key, terms in term_types.items():
            match_on, label = key

            if match_on.lower() == 'regex':
                self.add_regex_matcher(terms, label)

            else:
                self.add_phrase_matcher(terms, label, match_on)

    def add_phrase_matcher(self, terms, label, match_on):
        """Add phrase matcher to the term matchers."""
        if match_on not in self.matchers:
            self.matchers[match_on] = PhraseMatcher(
                self.nlp.vocab, attr=match_on)
        patterns = [self.nlp.make_doc(t['term']) for t in terms]
        self.matchers[match_on].add(label, self.enrich_tokens, *patterns)

    def add_regex_matcher(self, terms, label):
        """Add a regex matcher to the term matchers."""
        if 'regex' not in self.matchers:
            self.matchers['regex'] = Matcher(self.nlp.vocab)
        patterns = [[{'TEXT': {'REGEX': t['term']}}] for t in terms]
        self.matchers['regex'].add(
            label, patterns, on_match=self.enrich_tokens)

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
