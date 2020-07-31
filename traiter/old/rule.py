"""RuleList for parsing and rule builders."""

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Callable, Dict, List, Pattern, Union

import regex

from traiter.pylib.util import FLAGS

TOKEN = 0
SIZE = 4

# Find tokens in the regex. Look for words that are not part of a group
# name or a metacharacter. So, "word" not "<word>". Neither "(?P" nor "\b".
WORD = regex.compile(r"""
    (?<! \(\?P< ) (?<! \(\? ) (?<! [\\] )
    \b (?P<word> [a-z]\w* ) \b """, FLAGS)

Rules = List['Rule']
RuleDict = Dict[str, 'Rule']
Groups = Dict[str, Union[str, List[str]]]
Action = Callable[['Token'], Any]
InRegexp = Union[str, List[str]]

FIRST = -9999
SECOND = -9990
LOWEST = 9999


class RuleType(IntEnum):
    """What type of a rule are we dealing with."""

    SCANNER = 1
    GROUPER = 2
    REPLACER = 3
    PRODUCER = 4


@dataclass
class Rule:  # pylint: disable=too-many-instance-attributes
    """Create a rule."""

    name: str               # Unique within a catalog but not across catalogs
    pattern: str            # The regex before it is manipulated
    type: RuleType
    token: str
    action: Action = None   # What to do when there is a match
    regexp: Pattern = None  # The compiled regexp
    capture: bool = True    # Will the rule create an outer capture group?
    priority: int = 0       # When should the rule be triggered: FIRST? LAST?

    def __lt__(self, other: 'Rule'):
        """Custom sort order."""
        return (self.type, self.priority) < (other.type, other.priority)

    def __eq__(self, other):
        """Compare tokens for tests."""
        fields = ('name', 'pattern', 'type', 'action', 'capture', 'priority')
        you = tuple(v for k, v in other.__dict__.items() if k in fields)
        me_ = tuple(v for k, v in self.__dict__.items() if k in fields)
        return me_ == you

    def build(self, rules: RuleDict) -> str:
        """Build regular expressions for token matches."""

        def _rep(match):
            word = match.group('word')
            if word not in rules:
                print(f'Error: In "{self.name}", {word}" is not defined.')
            sub = rules.get(word)

            if sub.type == RuleType.SCANNER:
                return fr'(?: {sub.token} )'

            return sub.regexp.pattern

        regexp = WORD.sub(_rep, self.pattern)

        if self.capture:
            return fr'(?P<{self.name}> {regexp} )'
        return fr'(?: {regexp} )'

    def compile(self, rules: RuleDict):
        """Build and compile a rule."""
        pattern = self.build(rules)
        self.regexp = regex.compile(pattern, FLAGS)


def next_token() -> str:
    """Get the next token."""
    global TOKEN  # pylint: disable=global-statement
    TOKEN += 1
    return f'{TOKEN:04x}'


def join(regexp: InRegexp) -> str:
    """Build a single regexp from multiple strings."""
    if isinstance(regexp, (list, tuple, set)):
        regexp = ' | '.join(regexp)
    return ' '.join(regexp.split())


def part(
        name: str,
        regexp: InRegexp,
        action: Action = None,
        capture: bool = True,
        priority: int = 0) -> Rule:
    """Build a regular expression with a named group."""
    pattern = join(regexp)
    regexp = f'(?P<{name}> {pattern} )' if capture else f'(?: {pattern} )'
    regexp = regex.compile(regexp, FLAGS)
    return Rule(
        name=name,
        pattern=pattern,
        type=RuleType.SCANNER,
        token=next_token(),
        action=action,
        regexp=regexp,
        priority=priority)


def term(
        name: str,
        regexp: InRegexp,
        action: Action = None,
        capture: bool = True,
        priority: int = 0) -> Rule:
    r"""Wrap a regular expression in \b character classes."""
    pattern = join(regexp)
    regexp = f'(?P<{name}> {pattern} )' if capture else f'(?: {pattern} )'
    regexp = regex.compile(fr'\b {regexp} \b', FLAGS)
    return Rule(
        name=name,
        pattern=pattern,
        type=RuleType.SCANNER,
        token=next_token(),
        action=action,
        regexp=regexp,
        priority=priority)


def grouper(
        name: str,
        regexp: InRegexp,
        action: Action = None,
        capture: bool = True,
        priority: int = 0) -> Rule:
    """Build a grouper regular expression."""
    return Rule(
        name=name,
        pattern=join(regexp),
        type=RuleType.GROUPER,
        token=next_token(),
        action=action,
        capture=capture,
        priority=priority)


def replacer(
        name: str,
        regexp: InRegexp,
        action: Action = None,
        capture: bool = True,
        priority: int = 0) -> Rule:
    """Build a replacer regular expression."""
    return Rule(
        name=name,
        pattern=join(regexp),
        type=RuleType.REPLACER,
        token=next_token(),
        action=action,
        capture=capture,
        priority=priority)


def producer(
        action: Action,
        regexp: InRegexp,
        name: str = None,
        capture: bool = False,
        priority: int = 0) -> Rule:
    """Build a product regular expression."""
    token = next_token()
    name = name if name else f'producer_{token}'

    return Rule(
        name=name,
        pattern=join(regexp),
        type=RuleType.PRODUCER,
        token=token,
        action=action,
        capture=capture,
        priority=priority)
