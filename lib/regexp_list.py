"""An ordered list of regular expressions."""

import regex   # re expressions lack desired features
from lib.regexp import Regexp


class RegexpList:
    """An ordered list of regular expressions."""

    def __init__(
            self,
            args,
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
        self.args = args
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

        self.regexp_list = []
        self.parse_units = parse_units

    def _excluded_(self, match):
        if self.exclude_pattern and match and isinstance(match['value'], str):
            return self.exclude_pattern.search(match['value'])
        return False

    def append(self, *args, **kwargs):
        """Append a new regular expression to the regexp_list."""
        regexp = Regexp(*args, **kwargs)
        self.regexp_list.append(regexp)
        regexp.parse_units = self.parse_units
        regexp.units_from_key = self.units_from_key

    def parse(self, strings):
        """Parse a set of strings and return the first match."""
        for regexp in self.regexp_list:
            for idx, string in enumerate(strings):
                match = regexp.matches(string)
                if match and not self._excluded_(match):
                    match['regex'] = regexp.name
                    match['field'] = self.args.columns[idx]
                    return match
        return None
