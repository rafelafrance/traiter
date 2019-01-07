"""Parse sex notations."""

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

        # These are words that indicate "sex" is not a key
        skip = rx.kwd('and') | rx.kwd('is') | rx.kwd('was')

        parser = (
            (keyword + sex_q('value'))
            | (keyword + sex('value'))
            | (keyword + ~FollowedBy(skip) + Word(alphanums)('value'))
            | sex_q('value')
            | sex('value')
        )

        ignore = Word(rx.punct, excludeChars='.;?')
        parser.ignore(ignore)
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        if isinstance(match[0].value, str):
            value = self.normalize(match[0].value)
        else:
            values = match[0].value
            value = self.normalize(values[0])
            value += values[1] if len(values) > 1 else ''
        return Result(value=value, start=match[1], end=match[2])

    @staticmethod
    def normalize(value):
        """Normalize the value."""
        value = value.lower()
        value = 'female' if value[0] == 'f' else value
        return value
