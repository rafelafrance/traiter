"""Build catalogs of terms and their parts for sharing."""

import csv
import sys
from collections import defaultdict

from .pattern import Pattern, Type


class Catalog:
    """Build a catalogs of patterns."""

    def __init__(self, other: 'Catalog' = None) -> None:
        self.patterns = dict(other.patterns) if other else {}

    def __getitem__(self, name):
        """Emulate dict access of the rules."""
        return self.patterns[name]

    def __iter__(self):
        """Loop over the term values."""
        yield from self.patterns.values()

    def has(self, name, type_=None):
        """Check if the name is in the patterns and it's the correct type."""
        pattern = self.patterns.get(name)
        if pattern is None:
            return False
        if type_ is None:
            return True
        if isinstance(type_, (list, tuple, set)):
            return pattern.type in type_
        return pattern.type == type_

    def active(self, matcher, type_):
        """Get active patterns for the given type."""
        return [p for p in self.patterns
                if self.has(p.name, type_) and p.name in matcher.active_terms]

    def expand_groupers(self):
        """Groups can have other groups inside them."""
        groups = {p.name: p for p in self if self.has(p.name, Type.GROUPER)}
        finished = {k: False for k in groups.keys()}

        for group in groups:
            group.compiled = group.pattern

        tries = 0
        while not all(v for v in finished.values()) and tries < 10:
            tries += 1
            for name, group in groups.items():
                if finished[name]:
                    continue
                compiled = self.expand_grouper(groups, name, finished)
                group.compiled = compiled

    def expand_grouper(self, groups, name, finished):
        """Incrementally compile a grouper pattern."""
        finished[name] = True
        words = groups[name].get_word_set('compiled')
        compiled = groups[name].compiled

        for word in words:
            if not self.has(word):
                print(f'Error: "{word}" is not defined.', file=sys.stderr)
            elif self.has(word, (Type.PHRASE, Type.REGEXP)):
                continue
            elif not self.has(word, Type.GROUPER):
                print(f'Error: cannot group "{word}".', file=sys.stderr)
            elif finished.get(word):
                compiled = compiled.replace(word, groups[word].compiled)
            else:
                finished[name] = False
        return compiled

    @staticmethod
    def join(pattern) -> str:
        """Build a single pattern from multiple strings."""
        if isinstance(pattern, (list, tuple, set)):
            pattern = ' | '.join(pattern)
        return ' '.join(pattern.split())

    def phrase(self, name, match_on, terms):
        """Setup a phrase mather for scanning with spacy."""
        pat = Pattern(name, Type.PHRASE, match_on=match_on, terms=terms)
        self.patterns[name] = pat
        return pat

    def regexp(self, name, pattern):
        """Setup a phrase mather for scanning with spacy."""
        pat = Pattern(name, Type.REGEXP, pattern=pattern)
        self.patterns[name] = pat
        return pat

    def grouper(self, name, pattern):
        """Setup a phrase mather for scanning with spacy."""
        pattern = self.join(pattern)
        pattern = f'(?:{pattern})'
        pat = Pattern(name, Type.GROUPER, pattern=pattern)
        self.patterns[name] = pat
        return pat

    def producer(self, action, pattern, name=''):
        """Setup a phrase mather for scanning with spacy."""
        name = name if name else action.__qualname__
        pattern = self.join(pattern)
        pat = Pattern(name, Type.PRODUCER, action=action, pattern=pattern)
        self.patterns[name] = pat
        return pat

    def read_terms(self, path):
        """Read terms from a file."""
        all_terms = defaultdict(list)
        with open(path) as term_file:
            reader = csv.DictReader(term_file)
            for term in reader:
                all_terms[(term['name'], term['match_on'])].append(term)

        for key, terms in all_terms.items():
            name, match_on = key
            self.phrase(name, match_on, terms)

    def get_term_replacements(self, matcher):
        """Get replacement values for the terms."""
        # TODO: It is possible to have 2+ terms mapping to different
        # TODO: replacements.
        replacements = {}
        for phrase in self.active(matcher, Type.PHRASE):
            for term in phrase.terms:
                if replace := term.get('replace'):
                    replacements[term['term']] = replace
        return replacements
