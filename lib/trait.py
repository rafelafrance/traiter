"""Build a parser trait result."""

# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals

from lib.traits.numeric_trait_mixin import NumericTraitMixIn


class Trait(NumericTraitMixIn):
    """Build a parse result."""

    def __init__(self, value=None, field='', start=0, end=0,
                 ambiguous_key=False, as_is=False, dimension='',
                 estimated_value=False, includes='', measured_from='',
                 side='', units=None, units_inferred=False):
        """Build a parse result."""
        self.value = value
        self.field = field
        self.start = start
        self.end = end
        self.ambiguous_key = ambiguous_key
        self.as_is = as_is
        self.dimension = dimension
        self.estimated_value = estimated_value
        self.includes = includes
        self.measured_from = measured_from
        self.side = side
        self.units = units
        self.units_inferred = units_inferred
        self.skipped = ''

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
