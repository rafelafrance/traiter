"""An ordered list of regular expressions."""

import regex   # re expressions lack desired features
from trait_parsers.parser_regex import ParserRegex


class ParserBattery:
    """
    An ordered list of regular expressions.

    We use a carefully ordered list of regular expressions to look for traits
    in the database. There is some logic for dealing with the entire list of
    regular expressions in this object.
    """

    def __init__(
            self,
            exclude_pattern=None,
            parse_units=False,
            units_from_key=None):
        """
        Build the list of regular expressions.

        exclude_pattern: A regular expression that removes some false positives
        parse_units:     Some traits have units & others, like sex, do not
        units_from_key:  A regular expression that extracts units from a key.
                         Like "totallengthinmillimeters"
        """
        self.exclude_pattern = exclude_pattern
        if exclude_pattern:
            self.exclude_pattern = regex.compile(
                exclude_pattern,
                regex.IGNORECASE | regex.VERBOSE)

        self.units_from_key = units_from_key
        if units_from_key:
            self.units_from_key = regex.compile(
                units_from_key,
                regex.IGNORECASE | regex.VERBOSE)

        self.battery = []
        self.parse_units = parse_units

    def _excluded_(self, match):
        if self.exclude_pattern and match and isinstance(match['value'], str):
            return self.exclude_pattern.search(match['value'])
        return False

    def append(self, *args, **kwargs):
        """Append a new regular expression to the battery."""
        regexp = ParserRegex(*args, **kwargs)
        self.battery.append(regexp)
        regexp.parse_units = self.parse_units
        regexp.units_from_key = self.units_from_key

    def parse(self, string):
        """
        Use this battery to parse a string.

        The first regular expression that matches wins.
        """
        for regexp in self.battery:
            match = regexp.matches(string)
            if match and not self._excluded_(match):
                return match
        return None
