"""Extract information for further analysis."""

import regex
from collections import deque
from typing import Tuple
from pylib.stacked_regex.rule import build, Rules, RuleDict, RuleType
from pylib.stacked_regex.rule import SEP, FLAGS
from pylib.shared.util import flatten
from pylib.stacked_regex.token import Token, Tokens, Groups


class Parser:
    """Container for the the parser arrays."""

    def __init__(self, rules: Rules, name: str = 'parser') -> None:
        """Build the parser."""
        self.name: str = name
        self.rules: RuleDict = {}
        self._built = False
        self._scanners: Rules = []
        self._producers: Rules = []
        self.__iadd__(rules)

    def __iadd__(self, rule_list) -> None:
        """Add rules to the parser."""
        self._built = False
        for rule in flatten(rule_list):
            self.rules[rule.name] = rule

    def parse(self, text: str) -> Tokens:
        """Extract information from the text."""
        if not self._built:
            self._build()

        tokens = scan(self._scanners, text)

        # for token in tokens:
        #     print(token)
        # print()

        if self._producers:
            tokens = produce(self._producers, tokens, text)

        return tokens

    def _build(self) -> None:
        """Build the regular expressions."""
        self._built = True
        self._scanners = [r for r in self.rules.values()
                          if r.type == RuleType.SCANNER]

        rules = [r for r in self.rules.values() if r.type != RuleType.SCANNER]
        for rule in rules:
            pattern = build(rule.name, rule.pattern, self.rules)
            rule.regexp = regex.compile(pattern, FLAGS)
            if rule.type == RuleType.PRODUCER:
                self._producers.append(rule)


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
    matches = [(r, r.regexp.finditer(text)) for r in rules]
    matches = [Token(match[0], match=m) for match in matches for m in match[1]]
    matches = sorted(matches, key=lambda m: (m.span[0], -m.span[1]))
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
    for key in match.match.capturesdict():
        for i, value in enumerate(match.match.captures(key)):
            start = match.match.starts(key)[i]
            end = match.match.ends(key)[i]
            idx1 = token_text[:start].count(SEP)
            idx2 = token_text[:end].count(SEP) - 1
            append_group(groups, key, text[tokens[idx1].start:tokens[idx2].end])

    token = Token(match.rule, span=span, groups=groups)
    return token, first_idx, last_idx


# def replace(rules: Rules, tokens: Tokens, text: str) \
#         -> Tuple[Tokens, bool]:
#     """Replace token combinations with another token."""
#     replaced = []
#     token_text = SEP.join([t.name for t in tokens]) + SEP
#     matches = get_matches(rules, token_text)
#     again = bool(matches)
#
#     prev_idx = 0
#     while matches:
#         match = matches.popleft()
#         token, first_idx, last_idx = merge_tokens(
#             match, tokens, text, token_text)
#         if token.action:
#             token.action(token)
#         if prev_idx != first_idx:
#             replaced += tokens[prev_idx:first_idx]
#         replaced.append(token)
#         prev_idx = last_idx
#         matches = remove_passed_over(matches, match)
#
#     if prev_idx != len(tokens):
#         replaced += tokens[prev_idx:]
#
#     return replaced, again
