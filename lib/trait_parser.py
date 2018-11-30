"""Common logic for all traits."""

import regex
from abc import ABC, abstractmethod
import lib.trait_parsers.common_regexp as common_regexp


class TraitParser(ABC):
    """Common logic for all traits."""

    unit_conversions = {}

    def __init__(self):
        """Add defaults for the measurements."""
        self.args = None
        self.regexp_list = None
        self.default_units = None
        self.preferred_value = None

    @abstractmethod
    def success(self, result):
        """Return this when the measurement is found."""

    @abstractmethod
    def fail(self):
        """Return this when the measurement is not found."""

    def parse(self, strings):
        """Look for the first string that parses successfully."""
        trait = self.regexp_list.parse(strings)
        return trait if trait else None

    def search(self, strings):
        """Search for a good parse in the strings."""
        parsed = self.parse(strings)
        return self.success(parsed) if parsed else self.fail()

    def preferred(self, preferred_value):
        """If there is a preferred value then return it."""
        preferred_value = preferred_value.strip()
        if preferred_value:
            return self.success({
                'regex': '',
                'field': self.preferred_value,
                'start': 0,
                'end': len(preferred_value),
                'value': preferred_value,
                'key': '_preferred_'})
        return None

    def keyword_search(self, strings, preferred_value=''):
        """Search for keyword traits."""
        preferred_value = self.preferred(preferred_value)
        return preferred_value if preferred_value else self.search(strings)

    def search_and_normalize(self, strings, preferred_value=''):
        """Search for a numeric value (or range) and normalize the results."""
        preferred_value = self.preferred(preferred_value)
        if preferred_value:
            return preferred_value

        parsed = self.parse(strings)
        if parsed:
            normalized = self.normalize(parsed)
            return self.success(normalized)
        return self.fail()

    def normalize(self, parsed):
        """Convert units to a common measurement."""
        if isinstance(parsed['units'], list):
            return self.handle_multiple_units(parsed)

        # Normal unit (optional) & value
        units = parsed.get('units', self.default_units)
        units = units.lower() if units else self.default_units
        parsed['is_inferred'] = (units[0] == '_') if units else True

        if len(parsed['value']) > 1 and \
                common_regexp.IS_FRACT.search(parsed['value'][1]):
            return self.handle_fractional_values(parsed, units)

        values = common_regexp.IS_CROSS.split(parsed['value'])
        if len(values) > 1:
            return self.handle_multiple_value(parsed, values, units)

        values = common_regexp.IS_RANGE.split(parsed['value'])
        if len(values) > 1:
            return self.handle_multiple_value(parsed, values, units)

        # Value is just a number and optional units like "3.1 g"
        parsed['value'] = self.multiply(
            values[0], self.unit_conversions[units])
        return parsed

    def handle_multiple_units(self, parsed):
        """Handle multiple units like lengths given as: 5 feet 3 inches."""
        parsed['is_inferred'] = False
        units = ' '.join(parsed['units']).lower()

        # Handle cases where the last value is a range: 4 lbs 2 - 4 ozs
        if len(common_regexp.IS_RANGE.split(parsed['value'][1])) > 1:
            upper = self.multiply(
                parsed['value'][0], self.unit_conversions[units][0])
            lower = common_regexp.IS_RANGE.split(parsed['value'][1])
            parsed['value'] = []
            parsed['value'].append(self.multiply(
                lower[0], self.unit_conversions[units][1]) + upper)
            parsed['value'].append(self.multiply(
                lower[1], self.unit_conversions[units][1]) + upper)

        # Handle cases like: 3 lbs 2 ozs
        else:
            value = self.multiply(
                parsed['value'][0], self.unit_conversions[units][0])
            value += self.multiply(
                parsed['value'][1], self.unit_conversions[units][1])
            parsed['value'] = value

        return parsed

    def handle_fractional_values(self, parsed, units):
        """Handle fractional values like 10 3/8 inches."""
        if not parsed['value'][0]:
            parsed['value'][0] = '0'
        value = self.multiply(parsed['value'][0], self.unit_conversions[units])
        fract = common_regexp.IS_FRACT.split(parsed['value'][1])
        value += float(fract[0]) / float(fract[1]) \
            * self.unit_conversions[units]
        parsed['value'] = round(value, 1)
        return parsed

    def handle_multiple_value(self, parsed, values, units):
        """Handle cases like: '3 - 5 mm' or 3 x 5 mm."""
        parsed['value'] = [
            self.multiply(values[0], self.unit_conversions[units]),
            self.multiply(values[1], self.unit_conversions[units])]
        return parsed

    @staticmethod
    def multiply(value, units):
        """Calculate the numeric value given the units."""
        value = regex.sub(r'[^\d\.]', '', value)
        precision = 0
        parts = value.split('.')
        if len(parts) > 1:
            precision = len(parts[1])
        result = round(float(value) * units, precision)
        return result if precision else int(result)
