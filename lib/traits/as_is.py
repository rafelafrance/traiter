"""Parse life stage notations."""

from pyparsing import Regex
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class AsIs(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        data = Regex(r' \S .* \S | \S', rx.flags)
        parser = data('value')
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        return Result(value=match[0].value, start=match[1], end=match[2])
