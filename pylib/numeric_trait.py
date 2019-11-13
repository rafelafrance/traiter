"""Functions for building a numeric trait."""

import re
from collections import namedtuple
from pylib.trait import Trait
from pylib.convert_units import convert
from pylib.shared_patterns import SHARED


ParseKey = namedtuple(
    'ParseKey', 'low high dimension includes measured_from side')


class NumericTrait(Trait):
    """Handle numeric traits values."""

    def merge_flags(self, other):
        """Capture the meaning across all parses."""
        super().merge_flags(other)

        units_inferred = bool(getattr(other, 'units_inferred'))
        units_inferred &= bool(getattr(other, 'units_inferred'))
        setattr(self, 'units_inferred', units_inferred)

        units_inferred = bool(getattr(other, 'estimated_value'))
        units_inferred &= bool(getattr(other, 'estimated_value'))
        setattr(self, 'estimated_value', units_inferred)

    def convert_value(self, units):
        """Set the units and convert_value the value."""
        if not units:
            setattr(self, 'units_inferred', True)
            setattr(self, 'units', None)
        else:
            setattr(self, 'units_inferred', False)
            if isinstance(units, list) and isinstance(self.values, list):
                units = [x.lower() for x in units]
                setattr(
                    self,
                    'value',
                    [convert(v, u) for v, u in zip(self.value, units)])
            else:
                units = units[0] if isinstance(units, list) else units
                units = units.lower()
                setattr(self, 'value', convert(self.value, units))
            setattr(self, 'units', units)

    @staticmethod
    def to_float(value):
        """Convert the value to a float."""
        value = re.sub(r'[^\d.]', '', value) if value else ''
        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def to_int(value):
        """Convert value to an integer, handle 'no' or 'none' etc."""
        value = re.sub(r'[^\d]', '', value) if value else ''
        try:
            return int(value)
        except ValueError:
            return 0

    def float_value(self, value1, value2=None):
        """Convert the value to a float before setting it."""
        value1 = self.to_float(value1)
        value2 = self.to_float(value2)
        setattr(self, 'value', value1)
        if value2:
            setattr(self, 'value', [value1, value2])

    def fraction_value(self, token):
        """Calculate a fraction value like: 10 3/8."""
        whole = self.to_float(token.groups.get('whole'))
        numerator = self.to_float(token.groups['numerator'])
        denominator = self.to_float(token.groups['denominator'])
        whole = whole if whole else 0
        setattr(self, 'value', whole + numerator / denominator)

    def compound_value(self, values, units):
        """Calculate value for compound units like: 5 lbs 4 ozs."""
        setattr(self, 'units', units)
        big = self.to_float(values[0])
        big = convert(big, units[0])
        range_joiner = SHARED['range_joiner'].pattern
        smalls = re.split(range_joiner, values[1])
        smalls = [self.to_float(x) for x in smalls]
        setattr(self, 'value', [big + convert(x, units[1]) for x in smalls])
        setattr(self, 'value', [round(v, 2) for v in self.value])
        setattr(self, 'units_inferred', False)
        if len(self.value) == 1:
            setattr(self, 'value', self.value[0])

    def cross_value(self, token):
        """Handle a value like 5 cm x 21 mm."""
        values = self.all_values(
            token, ['value1', 'value2a', 'value2b', 'value2c'])
        self.float_value(*values)

        units = self.all_values(
            token, ['units', 'units1a', 'units1b', 'units1c', 'units2'])
        self.convert_value(units)

    @staticmethod
    def all_values(token1, keys):
        """Get all the values into a single list."""
        values = []
        for key in keys:
            if token1.groups.get(key):
                value = token1.groups[key]
                values += value if isinstance(value, list) else [value]
        return values

    def first_value(self, token, keys):
        """Rake values and return the first one if there is any."""
        values = self.all_values(token, keys)
        return values[0] if values else None

    def as_key(self):
        """Do the parses describe the same trait."""
        low, high = self.value, ''
        if isinstance(self.value, list):
            low, high = self.value
            if low > high:
                low, high = high, low
        return ParseKey(
            low=low,
            high=high,
            dimension=self.dimension,
            includes=self.includes,
            measured_from=self.measured_from,
            side=self.side)
