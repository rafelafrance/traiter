"""Current state of the matcher."""

from dataclasses import dataclass


@dataclass
class State:
    """Matcher state saved to the backtrack stack."""
    token_idx: int = 0
    rule_idx: int = 0
    value_idx: int = 0
    repeat_idx: int = 0
    match_len: int = 0
