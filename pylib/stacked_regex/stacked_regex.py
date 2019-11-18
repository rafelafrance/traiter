"""
Extract information for further analysis.

All steps use regular expressions. Step 1 uses them on raw text like any
other regular expression but the other two steps use them on the token
stream. The regular expressions on the token stream look and behave just
like normal regular expressions but they are adjusted to work on tokens &
not text. I.e. steps 2 & 3 use a domain specific language (DSL) for the
token-level regular expressions.

This is a 3-step process:

1) Replace text with tokens. We use regular expressions to create a token
   stream from the raw text. During this process, any text that is not
   captured by a token regex is removed from the token stream, i.e. noise
   is removed from the text.

2) Replace tokens with other tokens. Use a DSL to capture sets of tokens that
   may be combined into a single token. This simplification step is often
   repeated so simplifications may be built up step-wise.

3) Replace tokens with the final tokens. Everything except the final tokens are
   removed. This final stream of tokens is what the client code processes.
"""

from dataclasses import dataclass, field
from collections import deque
from typing import Tuple
from pylib.stacked_regex.rule import Rules, SEP
from pylib.stacked_regex.token import Token, Tokens, Groups


@dataclass
class Parser:
    """Container for the the parser arrays."""

    name: str = 'parser'
    scanners: Rules = field(default_factory=list)
    replacers: Rules = field(default_factory=list)
    producers: Rules = field(default_factory=list)

    def parse(self, text: str) -> Tokens:
        """
        Extract information from the text.

        This is the 3-step process outlined above.
        """
        tokens = scan(self.scanners, text)
        again = bool(self.replacers)
        while again:
            tokens, again = replace(self.replacers, tokens, text)
        return produce(self.producers, tokens, text)


def scan(rules: Rules, text: str) -> Tokens:
    """Scan a string & return tokens."""
    tokens = []
    matches = get_matches(rules, text)

    while matches:
        token = matches.popleft()
        if token.action:
            token.action(token)
        tokens.append(token)
        matches = remove_passed_over(matches, token)
    return tokens


def replace(rules: Rules, tokens: Tokens, text: str) -> Tuple[Tokens, bool]:
    """Replace token combinations with another token."""
    replaced = []
    token_text = SEP.join([t.name for t in tokens]) + SEP
    matches = get_matches(rules, token_text)
    again = bool(matches)

    prev_idx = 0
    while matches:
        match = matches.popleft()
        token, first_idx, last_idx = merge_tokens(
            match, tokens, text, token_text)
        if token.action:
            token.action(token)
        if prev_idx != first_idx:
            replaced += tokens[prev_idx:first_idx]
        replaced.append(token)
        prev_idx = last_idx
        matches = remove_passed_over(matches, match)

    if prev_idx != len(tokens):
        replaced += tokens[prev_idx:]

    return replaced, again


def produce(rules: Rules, tokens: Tokens, text: str) -> Tokens:
    """Produce final tokens for consumption by the client code."""
    results = []
    token_text = SEP.join([t.name for t in tokens]) + SEP
    matches = get_matches(rules, token_text)

    while matches:
        match = matches.popleft()
        token, _, _ = merge_tokens(match, tokens, text, token_text)
        results.append(token)
        matches = remove_passed_over(matches, match)

    return results


def remove_passed_over(matches: deque, match: Token) -> deque:
    """Remove matches that have been skipped over by the current match."""
    while matches and matches[0].span[0] < match.span[1]:
        matches.popleft()
    return matches


def get_matches(rules: Rules, text: str) -> deque:
    """Get all of the text matches for the rules sorted by position."""
    matches = [(r, r.regex.finditer(text)) for r in rules]
    matches = [Token(match[0], match=m) for match in matches for m in match[1]]
    matches = sorted(matches, key=lambda m: m.span[0])
    return deque(matches)


def append_group(groups: Groups, key: str, value: str) -> None:
    """Append a group to the groups dictionary."""
    old = []
    if key in groups:
        old = groups[key] if isinstance(groups[key], list) else [groups[key]]
    new = value if isinstance(value, list) else [value]
    values = old + new
    groups[key] = values[0] if len(values) == 1 else values


def merge_tokens(match: Token, tokens: Tokens, text: str, token_text: str) \
        -> Tuple[Token, int, int]:
    """Merge all matched tokens into one token."""
    # Get tokens in match
    first_idx = token_text[:match.start].count(SEP)
    last_idx = token_text[:match.end].count(SEP)
    span = (tokens[first_idx].start, tokens[last_idx - 1].end)

    # Merge all subgroups from sub-tokens into current token
    groups = {}
    for token in tokens[first_idx:last_idx]:
        for key, value in token.groups.items():
            append_group(groups, key, value)

    # Add groups from current token with real (not tokenized) text
    for key in match.groups:
        idx1 = token_text[:match.match.start(key)].count(SEP)
        idx2 = token_text[:match.match.end(key)].count(SEP) - 1
        append_group(groups, key, text[tokens[idx1].start:tokens[idx2].end])

    token = Token(match.rule, span=span, groups=groups)
    return token, first_idx, last_idx
