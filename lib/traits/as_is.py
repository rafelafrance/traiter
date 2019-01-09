"""Parse life stage notations."""

from pyparsing import Regex
from lib.base_trait import BaseTrait
from lib.parse_result import ParseResult
import lib.shared_parser_patterns as sp


class AsIs(BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        data = Regex(r' \S .* \S | \S', sp.flags)
        parser = data('value')
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        return ParseResult(value=match[0].value, start=match[1], end=match[2])
