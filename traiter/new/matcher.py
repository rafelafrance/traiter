"""Match tokens against rules."""

from .rules.rule import Patterns
from .token import Token


def match(patterns: Patterns, tokens: Token):
    """Match tokens against patterns."""
