"""Numeric value logic for the parsed trait object."""

import re
from lib.convert_units import convert
import lib.shared_trait_patterns as stp


class ParsedNumericMixIn:
    """Handle parsed trait numeric values."""

    def convert_value(self, units):
        """Set the units and convert_value the value."""
        self.history.append((self.value, self.units))
        self.units = units
        if not units:
            self.flags['units_inferred'] = True
        else:
            if self.flags.get('units_inferred'):
                del self.flags['units_inferred']
            if isinstance(units, list):
                self.value = [convert(v, u) for v, u in zip(self.value, units)]
            else:
                self.value = convert(self.value, units)

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

    def fraction_value(self, values):
        """Calculate a fraction value like: 10 3/8."""
        whole = self.to_float(values.get('whole'))
        numerator = self.to_float(values['numerator'])
        denominator = self.to_float(values['denominator'])
        whole = whole if whole else 0
        self.value = whole + numerator / denominator

    def compound_value(self, values, units):
        """Calculate value for compound units like: 5 lbs 4 ozs."""
        self.units = units
        big = self.to_float(values[units[0]])
        big = convert(big, units[0])
        smalls = re.split(stp.pair_joiner, values[units[1]])
        smalls = [self.to_float(x) for x in smalls]
        self.value = [big + convert(x, units[1]) for x in smalls]
        if len(self.value) == 1:
            self.value = self.value[0]

    def cross_value(self, parts):
        """Handle a value like 5 cm x 21 mm."""
        self.float_value(parts.get('value1'), parts.get('value2'))
        units = parts.get('units')
        units = units if units else parts.get('units1')
        units2 = parts.get('units2')
        units = [units, units2] if units2 and units != units2 else units
        self.convert_value(units)
