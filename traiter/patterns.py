"""Handle spacy pattern sets."""

from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler


def add_matcher_patterns(matcher: Matcher, *patterns, greedy='LONGEST'):
    """Add patterns to a matcher."""
    for rule in patterns:
        matcher.add(
            rule['label'],
            rule['patterns'],
            on_match=rule.get('on_match'),
            greedy=greedy)


def add_ruler_patterns(ruler: EntityRuler, *patterns):
    """Add patterns to a ruler."""
    rules = []
    for matcher in patterns:
        for rule_set in matcher:
            label = rule_set['label']
            id_ = rule_set.get('id')
            for pattern in rule_set['patterns']:
                rule = {'label': label, 'pattern': pattern}
                if id_:
                    rule['id'] = id_
                rules.append(rule)

    ruler.add_patterns(rules)
