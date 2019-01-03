"""Parse life stage notations."""

from pyparsing import Regex
from lib.parsers.base import Base
import lib.parsers.regexp as rx


class AnyValue(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        data = Regex(r' \S .* \S | \S', rx.flags)
        parser = data('value')
        return parser
