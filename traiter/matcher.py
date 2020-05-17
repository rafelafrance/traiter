"""Common logic for parsing trait notations."""

from spacy.matcher import Matcher

from .nlp import NLP, RULER


class Parser:
    """Shared parser logic."""

    def __init__(self):
        self.trait_matchers = []    # Spacy matchers for traits
        self.actions = {}           # Action to take on a matched trait

    @staticmethod
    def add_terms(terms):
        """Add phrase matcher to the term matchers."""
        patterns = [{'label': t['label'], 'pattern': t['pattern']}
                    for t in terms if t['attr'].upper() != 'REGEX']
        RULER.add_patterns(patterns)

        patterns = [{'label': t['label'],
                     'pattern': [{'TEXT': {'REGEX': t['pattern']}}]}
                    for t in terms if t['attr'].upper() == 'REGEX']

        RULER.add_patterns(patterns)

    def add_patterns(self, rules):
        """Build matchers that recognize traits."""
        matcher = Matcher(NLP.vocab)
        self.trait_matchers.append(matcher)
        for label, rule in rules.items():
            patterns = rule['patterns']
            on_match = rule['on_match']
            matcher.add(label, patterns)
            self.actions[label] = on_match

    def parse(self, text):
        """Parse the traits."""
        doc = NLP(text)

        with doc.retokenize() as retokenizer:
            for ent in doc.ents:
                attrs = {'_': {'term': ent.label_}}
                retokenizer.merge(doc[ent.start:ent.end], attrs=attrs)

        matches = []
        for matcher in self.trait_matchers:
            matches += matcher(doc)

        matches = self.leftmost_longest(matches)

        with doc.retokenize() as retokenizer:
            for match in matches:
                match_id, start, end = match
                span = doc[start:end]
                trait = NLP.vocab.strings[match_id]
                attrs = self.actions[trait](span)
                attrs = {'_': {'trait': trait, 'data': attrs}}
                retokenizer.merge(span, attrs=attrs)

        # for token in doc:
        #     print(token._.trait, token._.data, token.text)

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
