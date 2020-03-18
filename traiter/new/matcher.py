"""Match tokens against rules."""

from dataclasses import dataclass, field
from typing import List
from .rules.rule import Patterns, Rule
from .token import Tokens
from .state import State


@dataclass
class Match:
    """Information about a match."""
    pattern_idx: int = 0
    token_start: int = 0
    token_end: int = 0
    token2rule: List[Rule] = field(default_factory=list)


def match(patterns: Patterns, tokens: Tokens) -> List[Match]:
    """Match tokens against patterns."""
    matches: List[Match] = []
    stack: List[State] = []

    token_idx: int = 0
    while token_idx < len(tokens):
        for pattern_idx, pattern in enumerate(patterns):
            rule_idx = 0
            token2rule = []
            token_start = token_idx
            state = State(token_start=token_start)

            while rule_idx < len(pattern):
                rule = pattern[rule_idx]
                success = rule.func(tokens, state)

                if success:
                    # A candidate match
                    stack.append(state)
                    token2rule.append((rule, state.total_len))
                    token_start += state.total_len
                    rule_idx += 1
                    state = State(rule_idx=rule_idx, token_start=token_start)

                elif stack:
                    # The match failed so try backtracking
                    token2rule.pop()    # Get rid of the last mapping
                    state = stack.pop()

                else:
                    # All matches & backtracks failed so try next pattern
                    break

            else:
                # All rules in pattern passed so it's a match
                mapping = [r for r, t in token2rule for _ in range(t)]
                match_ = Match(pattern_idx, token_idx, token_start, mapping)
                matches.append(match_)
                token_idx = token_start - 1  # Handle += 1 below
                stack = []
                break  # Skip other rules

        token_idx += 1  # Try next token
    return matches
