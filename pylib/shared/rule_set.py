"""Build sets of rules."""

from pylib.stacked_regex.rule import Rules, fragment, keyword, grouper
from pylib.stacked_regex.rule import InRegexp


class RuleSet:
    """Build sets of rules."""

    def __init__(self, other: 'RuleSet' = None) -> None:
        """Create the rule set."""
        self.rules = dict(other.rules) if other else {}

    def add_frag(self, name: str, regexp: InRegexp, capture=True) -> None:
        """Add a rule to RULE."""
        self.rules[name] = fragment(name, regexp, capture=capture)

    def add_key(self, name: str, regexp: InRegexp, capture=True) -> None:
        """Add a rule to RULE."""
        self.rules[name] = keyword(name, regexp, capture=capture)

    def add_group(self, name: str, regexp: InRegexp, capture=True) -> None:
        """Add a rule to RULE."""
        self.rules[name] = grouper(name, regexp, capture=capture)

    def add_set(self, name: str, rules: Rules) -> None:
        """Add a rule set."""
        self.rules[name] = rules
