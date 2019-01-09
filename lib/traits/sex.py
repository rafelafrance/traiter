"""Parse sex notations."""

import re
from pyparsing import Word, alphanums, FollowedBy
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class Sex(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        keyword = rx.kwd('sex')

        sex = (rx.kwd('females') | rx.kwd('female')
               | rx.kwd('males') | rx.kwd('male'))
        sex_q = sex + Word('?')

        # These are words that indicate that "sex" is not a key
        skip = rx.kwd('and') | rx.kwd('is') | rx.kwd('was')

        parser = (
            (keyword + sex_q('value'))
            | (keyword + sex('value'))
            | (keyword + ~FollowedBy(skip) + Word(alphanums)('value'))
            | sex_q('value')
            | sex('value')
        )

        parser.ignore(Word(rx.punct, excludeChars='.;?'))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        result = Result()
        result.vocabulary_value(match[0].value)
        result.value = re.sub(r'\s*\?$', '?', result.value)
        result.value = re.sub(r'^(f\w*)', r'female', result.value)
        result.value = re.sub(r'^(m\w*)', r'male', result.value)
        result.ends(match[1], match[2])
        return result
