"""Build parser results."""

# pylint: disable=too-many-arguments

import re
from lib.convert_units import convert
import lib.shared_trait_patterns as stp


class ParsedTrait:
    """Build a parse result."""

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
        self._old_value = None

    def filtered_dict(self):
        """Remove hidden attributes from the __dict__."""
        return {k: v for k, v in self.__dict__.items() if k[0] != '_'}

    def __repr__(self):
        """Represent the result."""
        return 'ParsedTrait({})'.format(self.filtered_dict())

    def __eq__(self, other):
        """Compare results."""
        return self.filtered_dict() == other.filtered_dict()

    def convert_value(self, units):
        """Set the units and convert_value the value."""
        self._old_value = self.value
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

    def unset_units(self):
        """Rollback setting of units."""
        self.units = None
        self.value = self._old_value
        self.flags['units_inferred'] = True

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
