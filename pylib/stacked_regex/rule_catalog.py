"""Build catalogs of rules and their parts for sharing."""

from itertools import groupby
from pylib.shared.util import flatten
from pylib.stacked_regex.rule import Action, Rule, Rules, WORD
from pylib.stacked_regex.rule import part, term, grouper, producer, replacer
from pylib.stacked_regex.rule import InRegexp


class RuleCatalog:
    """
    Build a catalog of shared rules and what sub-patterns they need.

    The purpose of this object is to build a parts list of all patterns so that
    when we pull in one pattern we also automatically pull in all of its
    subordinate patterns without having to remember what they all are. For
    instance, if we have a grouper pattern like:

        grouper('value', ' len_range | number (?P<units> len_units )? ')

    We want to add a rule for the new 'value' grouper but we also want to make
    sure the 'len_range', 'number', and 'len_units' forms are also included.
    This is done recursively so, for example, the 'len_units' sub-grouper will
    also pull in the 'feet', 'inches', and 'metric_len' basal patterns.

    It is primarily used with shared patterns. We have catalogs of 100s of
    shared patterns and we only want to pull in (and search thru) the ones that
    are needed for a particular trait.
    """

    def __init__(self, other: 'RuleCatalog' = None) -> None:
        """Create the rule set."""
        self.rules = dict(other.rules) if other else {}

    def part(self, name: str, regexp: InRegexp, capture=True) -> None:
        """Add a partial term rule."""
        self.rules[name] = part(name, regexp, capture=capture)

    def term(self, name: str, regexp: InRegexp, capture=True) -> None:
        """Add a vocabulary term."""
        self.rules[name] = term(name, regexp, capture=capture)

    def grouper(self, name: str, regexp: InRegexp, capture=True) -> None:
        """Add a grouper rule."""
        rule = grouper(name, regexp, capture=capture)
        self.rules[name] = self._get_sub_patterns(rule)

    def replacer(self, name: str, regexp: InRegexp, capture=True) -> None:
        """Add a replacer rule."""
        rule = replacer(name, regexp, capture=capture)
        self.rules[name] = self._get_sub_patterns(rule)

    def producer(self, action: Action, regexp: InRegexp, capture=True) -> None:
        """Add a producer rule."""
        rule = producer(action, regexp, capture=capture)
        self.rules[rule.name] = self._get_sub_patterns(rule)

    def _get_sub_patterns(self, rule: Rule) -> Rules:
        rules = [self.rules[w] for w in WORD.findall(rule.pattern)]
        rules.append(rule)
        rules = flatten(rules)
        rules = sorted(rules, key=lambda r: r.type)
        return [list(g)[0] for _, g in groupby(rules, key=lambda r: r.name)]

    def add_set(self, name: str, rules: Rules) -> None:
        """Add a rule set."""
        self.rules[name] = rules
