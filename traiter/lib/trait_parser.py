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
        self.battery = None
        self.default_units = None

    @staticmethod
    @abstractmethod
    def success(result):
        """Return this when the measurement is found."""

    @staticmethod
    @abstractmethod
    def fail():
        """Return this when the measurement is not found."""

    def parse_first(self, strings):
        """Look for the first string that parses successfully."""
        string = '   |||   '.join(strings)
        if string:
            trait = self.parse(string)
            if trait:
                return trait
        return None

    def parse(self, string):
        """Apply the battery of regular expressions to a string."""
        string = '  '.join(self.WS_SPLIT.split(string.strip()))
        return self.battery.parse(string)

    def search(self, strings):
        """Search for a good parse in the strings."""
        parsed = self.parse_first(strings)
        if parsed:
            return self.success(parsed)
        return self.fail()

    def preferred_or_search(self, preferred, strings):
        """
        If there is a preferred value use it otherwise do a search.

        The preferred value is a column in the CSV file. If the row contains a
        value in the column's cell then return that value.
        """
        preferred = preferred.strip()
        if preferred:
            return self.success({'value': preferred})
        return self.search(strings)

    def search_and_normalize(self, strings):
        """Search for a good parse and normalize the results."""
        parsed = self.parse_first(strings)
        if parsed:
            normalized = self.normalize(parsed)
            return self.success(normalized)
        return self.fail()

    def normalize(self, parsed):
        """Convert units to a common measurement."""
        # Handle multiple units like lengths given as: 5 feet 3 inches
        if isinstance(parsed['units'], list):
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

        # Normal unit (optional) & value
        units = parsed.get('units', self.default_units)
        units = units.lower() if units else self.default_units
        parsed['is_inferred'] = (units[0] == '_') if units else True

        # Handle fractional values
        if len(parsed['value']) > 1 and \
                self.IS_FRACT.search(parsed['value'][1]):
            if not parsed['value'][0]:
                parsed['value'][0] = '0'
            value = self.multiply(
                parsed['value'][0], self.unit_conversions[units])
            fract = self.IS_FRACT.split(parsed['value'][1])
            value += float(fract[0]) / float(fract[1]) \
                * self.unit_conversions[units]
            parsed['value'] = round(value, 1)
            return parsed

        values = self.IS_RANGE.split(parsed['value'])
        if len(values) > 1:
            # Handle cases like: "3 - 5 mm"
            parsed['value'] = [
                self.multiply(values[0], self.unit_conversions[units]),
                self.multiply(values[1], self.unit_conversions[units])]
            return parsed

        # Value is just a number and optional units like "3.1 g"
        parsed['value'] = self.multiply(
            values[0], self.unit_conversions[units])
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

    common_regex_mass_length = r'''
        (?(DEFINE)

            # For our purposes numbers are always positive and decimals.
            (?P<number> (?&open) (?: \d{1,3} (?: , \d{3} ){1,3} | \d+ )
                (?: \. \d+ )? (?&close) [*]? )

            # We also want to pull in number ranges when appropriate.
            (?P<range> (?&number) (?: \s* (?: - | to ) \s* (?&number) )? )

            # Characters that follow a keyword
            (?P<key_end>  \s* [^ \w . \[ ( ]* \s* )

            # We sometimes want to guarantee no word precedes another word.
            # This cannot be done with negative look behind,
            # so we do a positive search for a separator
            (?P<no_word>  (?: ^ | [;,:"'\{\[\(]+ ) \s* )

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
