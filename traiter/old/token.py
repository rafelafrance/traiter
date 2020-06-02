"""A class to hold an individual token."""

# TODO: Delete me

from typing import Dict, List, Match, Tuple
from .rule import Rule, Action, Groups, SIZE

Tokens = List['Token']


class Token:
    """A token is the result of a rule match."""

    def __init__(
            self,
            rule: Rule = None,
            match: Match = None,
            group: Groups = None,
            span: Tuple[int, int] = None) -> None:
        """Create a token."""
        self.rule = rule
        self.match = match
        self.span = span if span else (0, 0)
        self.group = group if group else {}

        if match:
            self.span = match.span()
            self.group = {k: v for k, v in match.groupdict().items()
                          if v is not None}

    def __repr__(self) -> str:
        """Create string form of the object."""
        return '{}({})'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other: 'Token') -> bool:
        """Compare tokens."""
        return self.__dict__ == other.__dict__

    @property
    def __dict__(self) -> Dict:
        """Convert to a string."""
        return {
            'name': self.name,
            'span': self.span,
            'groups': self.group}

    @property
    def name(self) -> str:
        """Return the rule name."""
        return self.rule.name

    @property
    def start(self) -> int:
        """Return the match start."""
        return self.span[0]

    @property
    def end(self) -> int:
        """Return the match end."""
        return self.span[1]

    @property
    def action(self) -> Action:
        """Return the rule name."""
        return self.rule.action

    def valid_match(self) -> bool:
        """Make sure a token match is valid."""
        return self.span[0] % SIZE == 0
