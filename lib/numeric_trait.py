"""Functions for building a numeric trait."""

import re
from collections import namedtuple
from lib.trait import Trait
from lib.convert_units import convert
import lib.shared_tokens as tkn


ParseKey = namedtuple(
    'ParseKey', 'low high dimension includes measured_from side')


class NumericTrait(Trait):
    """Handle numeric traits values."""

    def __init__(self, **kwargs):
        """Build a numeric trait."""
        # Unit tests need these attributes to exist on the object
        super().__init__(**kwargs)

    def merge_flags(self, other):
        """Capture the meaning across all parses."""
        super().merge_flags(other)

        setattr(self, 'units_inferred', bool(self.units_inferred))
        self.units_inferred &= bool(other.units_inferred)

        setattr(self, 'estimated_value', bool(self.estimated_value))
        self.estimated_value |= bool(other.estimated_value)

    def convert_value(self, units):
        """Set the units and convert_value the value."""
        if not units:
            setattr(self, 'units_inferred', True)
        else:
            setattr(self, 'units_inferred', False)
            if isinstance(units, list):
                units = [x.lower() for x in units]
                setattr(
                    self,
                    'value',
                    [convert(v, u) for v, u in zip(self.value, units)])
            else:
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
        smalls = re.split(tkn.range_joiner, values[1])
        smalls = [self.to_float(x) for x in smalls]
        setattr(self, 'value', [big + convert(x, units[1]) for x in smalls])
        setattr(self, 'value', [round(v, 2) for v in self.value])
        setattr(self, 'units_inferred', False)
        if len(self.value) == 1:
            setattr(self, 'value', self.value[0])

    def cross_value(self, token):
        """Handle a value like 5 cm x 21 mm."""
        self.float_value(token.groups.get('value1'),
                         token.groups.get('value2'))
        units = token.groups.get('units')
        units = units if units else token.groups.get('units1')
        units2 = token.groups.get('units2')
        units = [units, units2] if units2 and units != units2 else units
        self.convert_value(units)

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
