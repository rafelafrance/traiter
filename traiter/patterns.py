"""Append patterns to pattern list from various input sources."""

from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional

PatternRulerType = List[Dict]
PatternMatcherType = DefaultDict[str, List[List[Dict]]]


class Patterns:
    """A list of patterns."""

    def __init__(self, patterns: Optional[PatternRulerType] = None) -> None:
        self.patterns: PatternRulerType = patterns if patterns else []

    def __iter__(self):
        yield from self.patterns

    def __add__(self, other: 'Patterns') -> 'Patterns':
        self.patterns += other.patterns
        return self

    def for_ruler(self) -> PatternRulerType:
        """Organize the patterns for a ruler."""
        return self.patterns

    def for_matcher(self) -> PatternMatcherType:
        """Organize the patterns for a matcher."""
        patterns = defaultdict(list)
        for pat in self.patterns:
            patterns[pat['label']].append(pat['pattern'])
        return patterns

    @classmethod
    def from_terms(cls, terms: List[Dict], attr: str = 'LOWER') -> 'Patterns':
        """Add patterns from terms.

        Add a pattern matcher for each term in the list.

        Each term is a dict with at least these three fields:
            1) label: what is the term's hypernym (ex. color)
            2) pattern: the phrase being matched (ex. gray-blue)
            3) attr: what spacy token field are we matching (ex. LOWER)
            ** There may be other fields in the dict but this method does not use them.
        """
        attr = attr.upper()
        rules = [{'label': t['label'], 'pattern': t['pattern']} for t in terms
                 if t['attr'].upper() == attr]
        return cls(rules)

    @classmethod
    def from_matchers(cls, *matchers) -> 'Patterns':
        """Build rules from matchers.

        Matchers are a list of dicts.
        The dict contains these fields:
            1) A "label" for the match.
            2) An optional function used to attach data to the entity.
            3) An "id" used to add extra data to the match.
            4) A list of spacy patterns. Each pattern is its own list.
        """
        rules = []
        for matcher in matchers:
            for rule_set in matcher:
                label = rule_set['label']
                id_ = rule_set.get('id')
                for pattern in rule_set['patterns']:
                    rule = {'label': label, 'pattern': pattern}
                    if id_:
                        rule['id'] = id_
                    rules.append(rule)

        return cls(rules)
