"""Rules for parsing and rule builders."""

import regex
from enum import Enum
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Pattern, Union
import inspect


SEP = ';'
FLAGS = regex.VERBOSE | regex.IGNORECASE

# Find tokens in the regex. Look for words that are not part of a group
# name or a metacharacter. So, "word" not "<word>". Neither "(?P" nor "\b".
WORD = regex.compile(r"""
    (?<! \(\?P< ) (?<! \(\? ) (?<! [\\] )
    \b (?P<word> [a-z]\w* ) \b """, regex.VERBOSE | regex.IGNORECASE)
# Find all tokens in the regex. Anything that is not a group name
# or a regexp metacharacter


Rules = List['Rule']
RuleDict = Dict[str, 'Rule']
Groups = Dict[str, Union[str, List[str]]]
Action = Callable[['Token'], Any]
InRegexp = Union[str, List[str]]


class RuleType(Enum):
    """What type of a rule are we dealing with."""

    SCANNER = 1
    REPLACER = 2
    PRODUCER = 3


@dataclass
class Rule:
    """Create a rule."""

    name: str
    pattern: str
    type: RuleType
    action: Action = None
    regexp: Pattern = None


def build(name: str, pattern: str, rules: RuleDict) -> str:
    """Build regular expressions for token matches."""
    def rep(match):
        sub = rules[match.group('word')]
        if sub.type == RuleType.SCANNER:
            return fr'(?: \b {sub.name}{SEP} )'
        return sub.regexp.pattern
    regexp = WORD.sub(rep, pattern)
    return fr'(?P<{name}> {regexp} )'


def join(regexp: InRegexp) -> str:
    """Build a single regexp from multiple strings."""
    if isinstance(regexp, list):
        regexp = ' | '.join(regexp)
    return ' '.join(regexp.split())


def fragment(name: str, regexp: InRegexp, action: Action = None) -> Rule:
    """Build a regular expression with a named group."""
    pattern = join(regexp)
    regexp = regex.compile(f'(?P<{name}> {pattern} )', FLAGS)
    return Rule(
        name=name,
        pattern=pattern,
        type=RuleType.SCANNER,
        action=action,
        regexp=regexp)


def keyword(name: str, regexp: InRegexp, action: Action = None) -> Rule:
    r"""Wrap a regular expression in \b character class."""
    pattern = join(regexp)
    regexp = regex.compile(fr'\b (?P<{name}> {pattern} ) \b', FLAGS)
    return Rule(
        name=name,
        pattern=pattern,
        type=RuleType.SCANNER,
        action=action,
        regexp=regexp)


def replacer(name: str, regexp: InRegexp, action: Action = None) -> Rule:
    """Build a replacer regular expression."""
    return Rule(
        name=name,
        pattern=join(regexp),
        type=RuleType.REPLACER,
        action=action)


def producer(action: Action, regexp: InRegexp, name: str = None) -> Rule:
    """Build a product regular expression."""
    if not name:
        frame = inspect.stack()[1]
        name = inspect.getmodule(frame[0]).__name__.replace('.', '_')
        line_no = frame.lineno
        name = f'{name}_{line_no}'

    return Rule(
        name=name,
        pattern=join(regexp),
        type=RuleType.PRODUCER,
        action=action)
