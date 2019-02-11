"""Build a parser trait result."""

# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals

from lib.numeric_parse_mixin import NumericParseMixIn


class Parse(NumericParseMixIn):
    """Build a parse result."""

    def __init__(self, value=None, field='', start=0, end=0,
                 ambiguous_key=False, as_is=False, dimension='',
                 estimated_value=False, includes='', measured_from='',
                 side='', units=None, units_inferred=False):
        """Build a parse result."""
        self.value = value                  # Normalized value
        self.field = field                  # Which CSV field was matched
        self.start = start                  # Match start position
        self.end = end                      # Match end position
        self.ambiguous_key = ambiguous_key  # Key may have different meaning?
        self.as_is = as_is                  # Is measurement taken as is?
        self.dimension = dimension          # Length, width, etc.
        self.estimated_value = estimated_value  # Is value noted as estimated?
        self.includes = includes                # Claw, etc.
        self.measured_from = measured_from      # Crown, notch, etc.
        self.side = side                        # Left, right, 1, 2, etc.
        self.units = units                      # Original units in notation
        self.units_inferred = units_inferred    # Were units found or guessed?
        self.skipped = ''                       # If the trait is skipped, why?

    def __repr__(self):
        """Represent the result."""
        return '{}({})'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        """Compare traits."""
        return self.__dict__ == other.__dict__

    def is_flag_in_token(self, flag, token, rename=None):
        """Set a flag if it is found in the token's groups field."""
        if token.groups.get(flag):
            flag = rename if rename else flag
            setattr(self, flag, True)

    def is_value_in_token(self, flag, token, rename=None):
        """Set a flag if it is found in the token's groups field."""
        value = token.groups.get(flag)
        if value:
            flag = rename if rename else flag
            setattr(self, flag, value.lower())
