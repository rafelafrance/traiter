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
        return self.patterns.get(name)

    def __iter__(self):
        """Loop over the term values."""
        yield from self.patterns.values()

    def has(self, name, type_):
        """Check if the name is in the patterns and it's the correct type."""
        pattern = self.patterns.get(name)
        if pattern is None:
            return False
        if type_ is None:
            return True
        if isinstance(type_, (list, tuple, set)):
            return pattern.type in type_
        return pattern.type == type_

    def expand_groupers(self, groupers):
        """Groups can have other groups inside them."""
        groups = {p.name: p for p in groupers}
        finished = {k: False for k in groups.keys()}

        for group in groups.values():
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
            if not self[word]:
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

    def phrase(self, name, attr, terms):
        """Setup a phrase matcher for scanning with spacy."""
        pat = Pattern.phrase(name, attr, terms)
        self.patterns[name] = pat
        return pat

    def regexp(self, name, pattern):
        """Setup a regexp matcher for scanning with spacy."""
        pat = Pattern.regexp(name, pattern)
        self.patterns[name] = pat
        return pat

    def grouper(self, name, pattern):
        """Setup a grouper pattern for parsing with regex."""
        pat = Pattern.grouper(name, pattern)
        self.patterns[name] = pat
        return pat

    def capture(self, name, pattern):
        """Setup a capture grouper pattern for parsing with regex."""
        pat = Pattern.capture(name, pattern)
        self.patterns[name] = pat
        return pat

    def producer(self, action, pattern, name=''):
        """Setup a producer pattern for parsing with regex."""
        pat = Pattern.producer(action, pattern, name)
        self.patterns[name] = pat
        return pat

    def read_terms(self, path):
        """Read terms from a file."""
        all_terms = defaultdict(list)
        with open(path) as term_file:
            reader = csv.DictReader(term_file)
            for term in reader:
                attr = term['attr'].upper()
                all_terms[(term['type'], attr)].append(term)

        for key, terms in all_terms.items():
            name, attr = key
            if attr == 'REGEX':
                self.regexp(name, [t['term'] for t in terms])
            else:
                self.phrase(name, attr, terms)
