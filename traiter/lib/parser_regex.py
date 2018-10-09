import regex   # re expressions lack desired features


class ParserRegex:
    """
    The regular expressions require common support logic so they are packaged into this object.
    We will use an array of these objects for the actual parsing.
    """

    def __init__(self, name, regexp, want_array=0, parse_units=False, default_key=None,
                 default_units=None, units_from_key=None, compound_value=False):
        """
        name:           Is a label used for debugging
        regexp:         The payload
        want_array:     Used to return an array of values but only up to the given length
        parse_units:    Some traits have units, like length, and others, like sex, do not
        default_key:
        default_units:
        units_from_key: A regular expression that will extract the units from a key. Like "totallengthinmillimeters"
        compound_value: Is the value in a form like "3 ft 7 in"
        """
        self.name = name
        self.regexp = regex.compile(regexp, regex.IGNORECASE | regex.VERBOSE)
        self.want_array     = want_array
        self.parse_units    = parse_units
        self.default_key    = default_key
        self.default_units  = default_units
        self.compound_value = compound_value
        self.units_from_key = units_from_key

    def _get_key_(self, match):
        key = None
        if 'key' in match.groupdict().keys():
            key = match.group('key')
        if not key:
            key = self.default_key
        return key

    def _get_value_(self, match):
        if 'value' in match.groupdict().keys():
            return match.group('value')
        return [match.group('value1'), match.group('value2')]

    def _get_units_(self, match, key):
        units = None
        if 'units' in match.groupdict().keys():
            units = match.group('units')
        if 'units1' in match.groupdict().keys():
            units = [match.group('units1'), match.group('units2')]
        if not units and key:
            u = self.units_from_key.search(key)
            if u:
                units = u.group('units')
        if not units:
            units = self.default_units
        return units

    def _get_value_array_(self, string):
        matches = self.regexp.findall(string)
        if matches and len(matches) <= self.want_array:
            return dict(key=None, value=matches)
        else:
            return None

    def matches(self, string):
        """Does this string match the regular expression? If so, then return a dictionary with the matched parts."""
        if self.want_array:
            return self._get_value_array_(string)

        match = self.regexp.search(string)
        if not match:
            return None

        parsed = dict(key=self._get_key_(match), value=self._get_value_(match))
        if self.parse_units:
            parsed['units'] = self._get_units_(match, parsed['key'])

        return parsed
