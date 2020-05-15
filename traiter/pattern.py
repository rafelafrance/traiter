"""Operations on various pattern types."""

from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Callable, Dict, List

import regex

from .nlp import NLP
from .util import FLAGS

CODE_LEN = 5
CODES = defaultdict(lambda: f'{len(CODES) + 1:04x}_')

# Find tokens in the regex. Look for words that are not part of a group
# name or a metacharacter. So, "word" not "<word>". Neither "(?P" nor "\b".
WORD = regex.compile(r"""
    (?<! \(\?P< ) (?<! \(\? ) (?<! [\\] )
    \b (?P<word> [a-z]\w* ) \b """, FLAGS)


class Type(IntEnum):
    """What type of a rule are we dealing with."""

    PHRASE = 1
    REGEXP = 2
    GROUPER = 3
    # REPLACER = 4
    PRODUCER = 5


@dataclass
class Pattern:
    """Create a pattern."""
    name: str
    type: Type

    terms: List[Dict] = None
    action: Callable = None
    match_on: str = ''
    pattern: str = ''
    compiled: Any = None

    @staticmethod
    def join(pattern) -> str:
        """Build a single pattern from multiple strings."""
        if isinstance(pattern, (list, tuple, set)):
            pattern = ' | '.join(pattern)
        return ' '.join(pattern.split())

    @classmethod
    def phrase(cls, name, match_on, terms):
        """Setup a phrase mather for scanning with spacy."""
        return cls(name, Type.PHRASE, match_on=match_on, terms=terms)

    @classmethod
    def regexp(cls, name, pattern):
        """Setup a phrase mather for scanning with spacy."""
        return cls(name, Type.REGEXP, pattern=pattern)

    @classmethod
    def grouper(cls, name, pattern):
        """Setup a phrase mather for scanning with spacy."""
        pattern = cls.join(pattern)
        pattern = f'(?:{pattern})'
        return cls(name, Type.GROUPER, pattern=pattern)

    @classmethod
    def producer(cls, action, pattern, name=''):
        """Setup a phrase mather for scanning with spacy."""
        name = name if name else action.__qualname__
        pattern = cls.join(pattern)
        return cls(name, Type.PRODUCER, action=action, pattern=pattern)

    def get_word_set(self, field='pattern'):
        """Break the pattern into a word set."""
        string = getattr(self, field)
        return {m.group('word') for m in WORD.finditer(string)}

    def build_phrase(self):
        """Build a phrase pattern."""
        return [NLP.make_doc(t) for t in self.terms]

    def build_regexp(self):
        """Build a regexp pattern."""
        return [[{'TEXT': {'REGEX': t}}] for t in self.terms]

    def build_producer(self, groupers):
        """Build a producer pattern."""

        def _replace(match):
            word = match.group('word')
            return f'(?:{CODES[word]})'

        compiled = self.pattern

        groups = {w: groupers[w] for w in self.get_word_set() if w in groupers}
        for name, compiled in groups.items():
            compiled = compiled.replace(name, compiled)

        compiled = WORD.sub(_replace, compiled)
        compiled = ' '.join(compiled.split())
        self.compiled = regex.compile(compiled, FLAGS)
