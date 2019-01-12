"""Parse life stage notations."""

from pyparsing import Regex, ParserElement
from lib.base_trait import BaseTrait
from lib.parsed_trait import ParsedTrait
import lib.shared_trait_patterns as stp

ParserElement.enablePackrat()


class AsIs(BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        data = Regex(r' \S .* \S | \S', stp.flags)
        parser = data('value')
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        return ParsedTrait(
            value=match[0].value,
            flags={'as_is': True},
            start=match[1], end=match[2])
