"""Parse the notations."""

import re
from abc import abstractmethod
from typing import Any, List
from dataclasses import dataclass
import lib.parsers.regexp as rx
from lib.parsers.convert_units import convert


@dataclass
class Result:
    """This is a rule production."""

    value: Any
    has_units: bool = False
    ambiguous: bool = False
    trait: str = None
    field: str = None
    start: int = 0
    end: int = 0


Results = List[Result]


class Base:  # pylint: disable=no-self-use,unused-argument
    """Shared parser logic."""

    def __init__(self, args=None):
        """Initialize the parser."""
        self.args = args
        self.parser = self.build_parser()

    # #########################################################################
    # These methods are meant to be overridden

    @abstractmethod
    def build_parser(self):
        """Return the trait parser."""

    def result(self, match):
        """Convert parsed tokens into a result."""
        if isinstance(match[0].value, str):
            value = match[0].value
        else:
            value = ' '.join(match[0].value)
        return Result(value=value.lower(), start=match[1], end=match[2])

    def post_parse(self, results: Results, args=None) -> Results:
        """Post-process the results."""
        return results

    # #########################################################################

    def parse(self, text: str) -> Results:
        """Parse the text."""
        results = []
        for match in self.parser.parseWithTabs().scanString(text):
            result = self.result(match)
            if result:
                results.append(result)
        return results

    def extended_parse(self, text: str, trait: str, field: str) -> Results:
        """Extend the results of the parse function with trait & field data."""
        results = self.parse(text)
        for result in results:
            result.trait = trait
            result.field = field
        return results

    # #########################################################################

    @staticmethod
    def to_float(value):
        """Convert string to float."""
        value = value.replace(',', '') if value else ''
        try:
            return float(value)
        except ValueError:
            return None

    def to_floats(self, text, splitter):
        """Split a string and return a list of floats."""
        text = text if text else ''
        return [self.to_float(x) for x in re.split(splitter, text)]

    def english_value(self, parts, major, minor):
        """Calculate value for english units."""
        big = self.to_floats(parts[major], rx.pair_joiner)
        small = self.to_floats(parts[minor], rx.pair_joiner)
        value = [convert(x, major) + convert(y, minor)
                 for x in big for y in small]
        if len(value) == 1:
            value = value[0]
        return value
