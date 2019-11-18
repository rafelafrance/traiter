"""Rules for parsing and rule builders."""

import regex
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Pattern, Union


SEP = ';'
FLAGS = regex.VERBOSE | regex.IGNORECASE


Rules = List['Rule']
Groups = Dict[str, str]
Action = Callable[['Token'], Any]
InRegexp = Union[str, List[str]]


@dataclass
class Rule:
    """Create a rule."""

    name: str
    regex: Pattern
    pattern: str
    action: Action = None


def simple_search(rule: Rule, text: str) -> Groups:
    """Search a string using this rule and return a dict."""
    match = rule.regex.search(text)
    groups = match.groupdict() if match else {}
    return {k: v for k, v in groups.items() if v is not None}


def tokenize_regex(regexp: str) -> str:
    """Replace names in regex with their tokens."""
    # Find tokens in the regex. Look for words that are not part of a group
    # name or a metacharacter. So, "word" not "<word>". Neither "(?P" nor "\b".
    word = regex.compile(r"""
        (?<! \(\?P< ) (?<! \(\? ) (?<! [\\] )
        \b (?P<word> [a-z]\w* ) \b """, FLAGS)
    # Find all tokens in the regex. Anything that is not a group name
    # or a regex metacharacter
    return word.sub(fr'(?: \g<word>{SEP} )', regexp)


def build(regexp: InRegexp) -> str:
    """Build a single regex from multiple strings."""
    if isinstance(regexp, list):
        regexp = ' | '.join(regexp)
    return ' '.join(regexp.split())


def fragment(name: str, regexp: InRegexp, action: Action = None) -> Rule:
    """Build a regular expression with a named group."""
    pattern = build(regexp)
    regexp = regex.compile(f'(?P<{name}> {pattern} )', FLAGS)
    return Rule(name=name, regex=regexp, pattern=pattern, action=action)


def keyword(name: str, regexp: InRegexp, action: Action = None) -> Rule:
    r"""Wrap a regular expression in \b character class."""
    pattern = build(regexp)
    regexp = regex.compile(fr'\b (?P<{name}> {pattern} ) \b', FLAGS)
    return Rule(name=name, regex=regexp, pattern=pattern, action=action)


def replacer(name: str, regexp: InRegexp, action: Action = None) -> Rule:
    """Build a replacer regular expression."""
    pattern = build(regexp)
    regexp = tokenize_regex(pattern)
    regexp = regex.compile(fr' \b (?P<{name}> {regexp} ) ', FLAGS)
    return Rule(name=name, regex=regexp, pattern=pattern, action=action)


def producer(action: Action, regexp: InRegexp, name: str = 'producer') -> Rule:
    """Build a product regular expression."""
    pattern = build(regexp)
    regexp = tokenize_regex(pattern)
    regexp = regex.compile(fr' \b (?: {regexp} ) ', flags=FLAGS)
    return Rule(name=name, action=action, regex=regexp, pattern=pattern)
