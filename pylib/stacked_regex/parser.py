"""Extract information for further analysis."""

from collections import deque
from typing import Tuple
from pylib.stacked_regex.rule import Rule, Rules, RuleType, SEP
from pylib.stacked_regex.token import Token, Tokens, Groups


class Parser:
    """Container for the the parser arrays."""

    def __init__(self, rules: Rules, name: str = 'parser') -> None:
        """Build the parser."""
        self.name = name
        self.scanners = []
        self.replacers = []
        self.producers = []
        self.__iadd__(rules)

    def __iadd__(self, rules) -> None:
        """Add rules to the parser."""
        for rule in rules if isinstance(rules, list) else [rules]:
            if isinstance(rule, list):
                for one in rule:
                    self._add_rule(one)
            else:
                self._add_rule(rule)

    def _add_rule(self, rule):
        """Add the rule to the correct array."""
        if rule.type == RuleType.SCANNER:
            self.scanners.append(rule)
        elif rule.type == RuleType.REPLACER:
            self.replacers.append(rule)
        elif rule.type == RuleType.PRODUCER:
            self.producers.append(rule)

    def parse(self, text: str) -> Tokens:
        """Extract information from the text."""
        tokens = scan(self.scanners, text)
        again = bool(self.replacers)
        while again:
            tokens, again = replace(self.replacers, tokens, text)
        # for token in tokens:
        #     print(token)
        # print()
        if self.producers:
            tokens = produce(self.producers, tokens, text)
        return tokens


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
