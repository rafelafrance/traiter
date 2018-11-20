"""Supporting logic for regular expressions."""

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments

import regex   # re expressions lack desired features


class Regexp:
    """Supporting logic for regular expressions."""

    def __init__(
            self,
            name,
            regexp,
            want_list=0,
            parse_units=False,
            default_key=None,
            default_units=None,
            units_from_key=None,
            compound_value=False):
        """
        Build the regular expression object.

        name:           Is a label used for debugging
        regexp:         The payload
        want_list:      Return a list of values but only up to the given length
        parse_units:    Some traits have units & others, like sex, do not
        default_key:
        default_units:
        units_from_key: A regular expression that extracts the units from a key
                        Like "totallengthinmillimeters"
        compound_value: Is the value in a form like "3 ft 7 in"
        """
        self.name = name
        self.regexp = regex.compile(regexp, regex.IGNORECASE | regex.VERBOSE)
        self.want_list = want_list
        self.parse_units = parse_units
        self.default_key = default_key
        self.default_units = default_units
        self.compound_value = compound_value
        self.units_from_key = units_from_key

    def _get_key(self, match):
        key = match.groupdict().get('key')
        return key if key else self.default_key

    @staticmethod
    def _get_value(match):
        val = match.groupdict().get('value')
        return val if val else [match.group('value1'), match.group('value2')]

    def _get_units(self, match, key):
        units = match.groupdict().get('units')

        if not units and match.groupdict().get('units1'):
            units = [match.group('units1'), match.group('units2')]

        if not units and key:
            units_from_key = self.units_from_key.search(key)
            if units_from_key:
                units = units_from_key.group('units')

        return units if units else self.default_units

    def _get_value_array(self, string):
        matches = self.regexp.finditer(string)

        values = []
        starts = []
        ends = []
        for idx, match in enumerate(matches):
            if idx >= self.want_list:
                return None
            values.append(match.group(0))
            starts.append(match.start())
            ends.append(match.end())
        if not values:
            return None
        starts = starts if len(starts) > 1 else starts[0]
        ends = ends if len(ends) > 1 else ends[0]

        if matches:
            return {'key': None,
                    'start': starts,
                    'end': ends,
                    'value': values}
        return None

    def matches(self, string):
        """Get a dictionary with the matched parts if it matches."""
        if self.want_list:
            return self._get_value_array(string)

        match = self.regexp.search(string)
        if not match:
            return None

        parsed = {'key': self._get_key(match),
                  'value': self._get_value(match),
                  'start': match.start(),
                  'end': match.end(),
                  'regex': self.name}

        if self.parse_units:
            parsed['units'] = self._get_units(match, parsed['key'])

        return parsed
