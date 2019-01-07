"""Parse the notations."""

import re
from abc import abstractmethod
import lib.regexp as rx
from lib.units import convert
from lib.result import Result


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
        raise NotImplementedError('You need to a build_parser function.')

    def result(self, match):
        """Convert parsed tokens into a result.

        This version works for some controlled vocabulary traits.
        """
        if isinstance(match[0].value, str):
            value = match[0].value
        else:
            value = ' '.join(match[0].value)
        return Result(value=value.lower(), start=match[1], end=match[2])

    # #########################################################################

    def parse(self, text: str, trait=None, field=None):
        """Parse the text."""
        results = []
        for match in self.parser.parseWithTabs().scanString(text):
            result = self.result(match)
            if result:
                result.trait = trait
                result.field = field
                results.append(result)
        return results

    # #########################################################################

    @staticmethod
    def to_float(value):
        """Convert string to float."""
        value = re.sub(r'[^\d.]', '', value) if value else ''
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

    @staticmethod
    def set_units_inferred(flags, units):
        """Set the units inferred flag."""
        if not units:
            flags['units_inferred'] = True

    @staticmethod
    def ambiguous_key(match):
        """Set the ambiguous key flag."""
        if 'ambiguous_key' in match[0].asList():
            return {'ambiguous_key': True}
        return {}

    @staticmethod
    def set_flag(parts, flags, key, as_bool=False):
        """Get the result flag from the parsed parts."""
        value = parts.get(key)
        if value:
            flags[key] = value
            if as_bool:
                flags[key] = bool(value)
