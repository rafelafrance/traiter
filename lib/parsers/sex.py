"""Parse sex notations."""

from pyparsing import Word, alphanums, FollowedBy
from pyparsing import CaselessKeyword as kw
from lib.parsers.base import Base, Result
import lib.parsers.regexp as rx


class Sex(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        keyword = kw('sex')

        sex = kw('females') | kw('female') | kw('males') | kw('male')
        sex_q = sex + Word('?')

        # These are words that indicate "sex" is not a key
        skip = kw('and') | kw('is') | kw('was')

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

    def post_process(self, results, args=None):
        """Post-process the results."""
        return results if len({r.value for r in results}) == 1 else []
