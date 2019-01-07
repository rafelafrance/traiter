"""Parse tail length notations."""

# from pyparsing import Regex, Word, alphas, alphanums
# from pyparsing import CaselessLiteral as lit
from lib.base import Base
from lib.result import Result
# from lib.units import convert
# import lib.regexp as rx


class TailLength(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""

    def result(self, match):
        """Convert parsed tokens into a result."""
        return Result()
