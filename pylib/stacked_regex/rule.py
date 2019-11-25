"""Rules for parsing and rule builders."""

from enum import Enum
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Pattern, Union
import inspect
import regex


SEP = ';'
FLAGS = regex.VERBOSE | regex.IGNORECASE

# Find tokens in the regex. Look for words that are not part of a group
# name or a metacharacter. So, "word" not "<word>". Neither "(?P" nor "\b".
WORD = regex.compile(r"""
    (?<! \(\?P< ) (?<! \(\? ) (?<! [\\] )
    \b (?P<word> [a-z]\w* ) \b """, regex.VERBOSE | regex.IGNORECASE)

Rules = List['Rule']
RuleDict = Dict[str, 'Rule']
Groups = Dict[str, Union[str, List[str]]]
Action = Callable[['Token'], Any]
InRegexp = Union[str, List[str]]


class RuleType(Enum):
    """What type of a rule are we dealing with."""

    SCANNER = 1
    GROUPER = 2
    REPLACER = 3
    PRODUCER = 4


@dataclass
class Rule:
    """Create a rule."""

    name: str
    pattern: str
    type: RuleType
    action: Action = None
    regexp: Pattern = None
    capture: bool = True

    def build(self, rules: RuleDict) -> str:
        """Build regular expressions for token matches."""
        def rep(match):
            word = match.group('word')
            if word not in rules:
                print(f'Error: "{word}" is not defined.')
            sub = rules.get(word)

            if sub.type == RuleType.SCANNER:
                return fr'(?: \b {sub.name}{SEP} )'

            return sub.regexp.pattern

        regexp = WORD.sub(rep, self.pattern)

        if self.capture:
            return fr'(?P<{self.name}> {regexp} )'
        return fr'(?: {regexp} )'

    def compile(self, rules: RuleDict):
        """Build and compile a rule."""
        pattern = self.build(rules)
        self.regexp = regex.compile(pattern, FLAGS)


def join(regexp: InRegexp) -> str:
    """Build a single regexp from multiple strings."""
    if isinstance(regexp, list):
        regexp = ' | '.join(regexp)
    return ' '.join(regexp.split())


def fragment(
        name: str,
        regexp: InRegexp,
        action: Action = None,
        capture: bool = True) -> Rule:
    """Build a regular expression with a named group."""
    pattern = join(regexp)
    regexp = f'(?P<{name}> {pattern} )' if capture else f'(?: {pattern} )'
    regexp = regex.compile(regexp, FLAGS)
    return Rule(
        name=name,
        pattern=pattern,
        type=RuleType.SCANNER,
        action=action,
        regexp=regexp)


def keyword(
        name: str,
        regexp: InRegexp,
        action: Action = None,
        capture: bool = True) -> Rule:
    r"""Wrap a regular expression in \b character class."""
    pattern = join(regexp)
    regexp = f'(?P<{name}> {pattern} )' if capture else f'(?: {pattern} )'
    regexp = regex.compile(fr'\b {regexp} \b', FLAGS)
    return Rule(
        name=name,
        pattern=pattern,
        type=RuleType.SCANNER,
        action=action,
        regexp=regexp)


def grouper(
        name: str,
        regexp: InRegexp,
        action: Action = None,
        capture: bool = True) -> Rule:
    """Build a grouper regular expression."""
    return Rule(
        name=name,
        pattern=join(regexp),
        type=RuleType.GROUPER,
        action=action,
        capture=capture)


def replacer(
        name: str,
        regexp: InRegexp,
        action: Action = None,
        capture: bool = True) -> Rule:
    """Build a grouper regular expression."""
    return Rule(
        name=name,
        pattern=join(regexp),
        type=RuleType.REPLACER,
        action=action,
        capture=capture)


def producer(
        action: Action,
        regexp: InRegexp,
        name: str = None,
        capture: bool = False) -> Rule:
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
        action=action,
        capture=capture)
