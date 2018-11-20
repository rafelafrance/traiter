"""Common logic for all traits."""

from abc import ABC, abstractmethod
import regex


class TraitParser(ABC):
    """Common logic for all traits."""

    IS_RANGE = regex.compile(r'- | to', flags=regex.IGNORECASE | regex.VERBOSE)
    IS_FRACT = regex.compile(r'\/', flags=regex.IGNORECASE | regex.VERBOSE)
    WS_SPLIT = regex.compile(r'\s\s\s+')

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
                self.IS_FRACT.search(parsed['value'][1]):
            return self.handle_fractional_values(parsed, units)

        values = self.IS_RANGE.split(parsed['value'])
        if len(values) > 1:
            return self.handle_range_value(parsed, values, units)

        # Value is just a number and optional units like "3.1 g"
        parsed['value'] = self.multiply(
            values[0], self.unit_conversions[units])
        return parsed

    def handle_multiple_units(self, parsed):
        """Handle multiple units like lengths given as: 5 feet 3 inches."""
        parsed['is_inferred'] = False
        units = ' '.join(parsed['units']).lower()

        # Handle cases where the last value is a range: 4 lbs 2 - 4 ozs
        if len(self.IS_RANGE.split(parsed['value'][1])) > 1:
            upper = self.multiply(
                parsed['value'][0], self.unit_conversions[units][0])
            lower = self.IS_RANGE.split(parsed['value'][1])
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
        fract = self.IS_FRACT.split(parsed['value'][1])
        value += float(fract[0]) / float(fract[1]) \
            * self.unit_conversions[units]
        parsed['value'] = round(value, 1)
        return parsed

    def handle_range_value(self, parsed, values, units):
        """Handle cases like: "3 - 5 mm."""
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

    unit_conversions = {}

    short_patterns = r'''
        (?(DEFINE)

            # Characters that follow a keyword
            (?P<key_end>  \s* [^ \w . \[ ( ]* \s* )

            # We sometimes want to guarantee no word precedes another word.
            # This cannot be done with negative look behind,
            # so we do a positive search for a separator
            (?P<no_word>  (?: ^ | [;,:"'\{\[\(]+ ) \s* )

            # Look for an optional dash or space character
            (?P<dash>     [\s\-]? )
            (?P<dash_req> [\s\-]  )

            # Look for an optional dot character
            (?P<dot> \.? )

            # Numbers are sometimes surrounded by brackets or parentheses
            # Don't worry about matching the opening and closing brackets
            (?P<open>  [\(\[\{]? )
            (?P<close> [\)\]\}]? )
        )'''

    common_regex_mass_length = short_patterns + r'''
        (?(DEFINE)

            # For our purposes numbers are always positive and decimals.
            (?P<number> (?&open) (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ )
                (?: \. \d+ )? (?&close) [*]? )

            # We also want to pull in number ranges when appropriate.
            (?P<range> (?&number) (?: \s* (?: - | to ) \s* (?&number) )? )

            # Keywords that may precede a shorthand measurement
            (?P<shorthand_words> on \s* tag
                            | specimens?
                            | catalog
                            | measurements (?: \s+ [\p{Letter}]+)
                            | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
                            | meas [.,]? (?: \s+ \w+ \. \w+ \. )?
            )

            # Common keyword misspellings preceding shorthand measurements
            (?P<shorthand_typos>  mesurements | Measurementsnt )

            # Keys where we need units to know if it's for mass or length
            (?P<key_units_req> measurements? | body | total )

            # Characters that separate shorthand values
            (?P<shorthand_sep> [:\/\-] )

            # Used in shorthand notation for unknown values
            (?P<shorthand_unknown> [\?x] )
        )'''
