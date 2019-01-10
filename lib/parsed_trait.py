"""Build parser results."""

# pylint: disable=too-many-arguments,too-many-instance-attributes

from lib.parsed_numeric_mixin import ParsedNumericMixIn


class ParsedTrait(ParsedNumericMixIn):
    """Build a parse result."""

    hide = ('trait', 'history')

    def __init__(self, value=None, units=None, trait=None, field=None,
                 start=0, end=0, flags=None):
        """Build a parse result."""
        self.value = value
        self.units = units
        self.trait = trait
        self.field = field
        self.start = start
        self.end = end
        self.flags = flags if flags else {}
        self.history = []

    def as_dict(self):
        """Remove hidden attributes from __dict__."""
        return {k: v for k, v in self.__dict__.items() if k not in self.hide}

    def __repr__(self):
        """Represent the result."""
        return 'ParseResult({})'.format(self.as_dict())

    def __eq__(self, other):
        """Compare results."""
        return self.as_dict() == other.as_dict()

    def vocabulary_value(self, value):
        """Set a controlled vocabulary value."""
        if isinstance(value, str):
            self.value = value
        else:
            self.value = ' '.join(value)
        self.value = self.value.lower()

    def ends(self, start, end):
        """Fill in the start and end location of the result."""
        self.start = start
        self.end = end

    def is_flag_in_dict(self, dictn, check, flag=None):
        """Set a flag if it is found in the dict."""
        flag = flag if flag else check
        if dictn.get(check):
            self.flags[flag] = True

    def flag_from_dict(self, dictn, flag):
        """Set a flag if it is found in the dict."""
        value = dictn.get(flag)
        if value:
            self.flags[flag] = value
