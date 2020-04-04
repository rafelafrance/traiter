"""Common logic for parsing trait notations."""

from traiter.nlp import NLP


class Matcher:
    """Shared lexer logic."""

    def __init__(self, name=''):
        self.name = name
        self.term_matcher = None
        self.nlp = NLP

    @staticmethod
    def first_longest(matches):
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

    def parse(self, text):
        """Parse the traits."""
        raise NotImplementedError

    @staticmethod
    def term_label(_, doc, i, matches):
        """Add the term labels to the tokens."""
        match_id, start, end = matches[i]
        label = doc.vocab.strings[match_id]
        for token in doc[start:end]:
            token._.term = label
