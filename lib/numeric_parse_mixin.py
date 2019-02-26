"""Functions for building a numeric trait."""

import re
from lib.convert_units import convert
import lib.shared_tokens as tkn


class NumericParseMixIn:
    """Handle parsed trait numeric values."""

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
        smalls = re.split(tkn.pair_joiner, values[1])
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
