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
        """Build a numeric trait.

        units:           Original units in notation
        units_inferred:  Were units found or guessed?

        estimated_value: Did the reporter indicate this was an estimate
        is_shorthand:    Flag 99-99-99-99=99 shorthand notation
        dimension:       Length, width, etc.
        includes:        Claw, etc. What is included changes he meaning
        measured_from:   Crown, notch, etc.
        """
        super().__init__(**kwargs)

        self.units = kwargs.get('units', None)
        self.units_inferred = kwargs.get('units_inferred', False)

        self.estimated_value = kwargs.get('estimated_value', False)
        self.is_shorthand = kwargs.get('is_shorthand', False)
        self.dimension = kwargs.get('dimension', '')
        self.includes = kwargs.get('includes', '')
        self.measured_from = kwargs.get('measured_from', '')

    def merge_flags(self, other):
        """Capture the meaning across all parses."""
        super().merge_flags(other)
        self.units_inferred &= other.units_inferred
        self.estimated_value |= other.estimated_value

    def convert_value(self, units):
        """Set the units and convert_value the value."""
        if not units:
            self.units_inferred = True
        else:
            self.units_inferred = False
            if isinstance(units, list):
                units = [x.lower() for x in units]
                self.value = [convert(v, u) for v, u in zip(self.value, units)]
            else:
                units = units.lower()
                self.value = convert(self.value, units)
        self.units = units

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
        self.value = value1
        if value2:
            self.value = [value1, value2]

    def fraction_value(self, token):
        """Calculate a fraction value like: 10 3/8."""
        whole = self.to_float(token.groups.get('whole'))
        numerator = self.to_float(token.groups['numerator'])
        denominator = self.to_float(token.groups['denominator'])
        whole = whole if whole else 0
        self.value = whole + numerator / denominator

    def compound_value(self, values, units):
        """Calculate value for compound units like: 5 lbs 4 ozs."""
        self.units = units
        big = self.to_float(values[0])
        big = convert(big, units[0])
        smalls = re.split(tkn.range_joiner, values[1])
        smalls = [self.to_float(x) for x in smalls]
        self.value = [big + convert(x, units[1]) for x in smalls]
        self.value = [round(v, 2) for v in self.value]
        if len(self.value) == 1:
            self.value = self.value[0]

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
