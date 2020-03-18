"""Rules for matching tokens."""

from abc import abstractmethod
from typing import Any, List
from ..token import Tokens
from ..state import State


class Rule:
    """How to match tokens."""

    def __init__(self, **kwargs):
        """Create common rule attributes."""
        kwargs = kwargs if kwargs else {}

        # Values for the rule
        self.values: Any = kwargs.get('values')

        # What field to compare in the token
        self.field: str = kwargs.get('field', 'text')

        # Extra data for processing tokens matched by this rule
        self.aux: str = kwargs.get('aux', '')

    def __eq__(self, other):
        """Compare rules."""
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        """Create string form of the object."""
        return '{}({})'.format(self.__class__.__name__, self.__dict__)

    @abstractmethod
    def func(self, tokens: Tokens, state: State) -> bool:
        """Predicate action."""
        raise NotImplementedError


Pattern = List[Rule]
Patterns = List[Pattern]
