"""Current state of the matcher."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class State:
    """Matcher state saved to the backtrack stack."""
    token_start: int = 0
    rule_idx: int = 0
    first_time: bool = True
    repeat_idx: List[int] = field(default_factory=list)

    @property
    def match_len(self):
        """Get the total length of the match."""
        return sum(self.repeat_idx)
