"""Parse tail length notations."""

# from pyparsing import Regex, Word, alphas, alphanums
# from pyparsing import CaselessLiteral as lit
from lib.parsers.base import Base, Result
# import lib.parsers.regexp as rx
# from lib.parsers.units import convert


class TailLength(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""

    def result(self, match):
        """Convert parsed tokens into a result."""
        return Result()
