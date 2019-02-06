"""Build a parser trait result."""

# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals

from lib.numeric_trait_mixin import NumericTraitMixIn


class Trait(NumericTraitMixIn):
    """Build a parse result."""

    hide = ('trait', 'history')

    def __init__(self, value=None, field=None, start=0, end=0,
                 ambiguous_key=None, as_is=None, dimension=None,
                 estimated_value=None, includes=None, measured_from=None,
                 side=None, trait=None, units=None, units_inferred=None):
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
        self.trait = trait
        self.units = units
        self.units_inferred = units_inferred
        self.skipped = None
        self.history = []

    def as_dict(self):
        """Remove hidden attributes from __dict__."""
        return {k: v for k, v in self.__dict__.items()
                if v is not None and k not in self.hide}

    def __repr__(self):
        """Represent the result."""
        return '{}({})'.format(self.__class__.__name__, self.as_dict())

    def __eq__(self, other):
        """Compare traits."""
        return self.as_dict() == other.as_dict()

    def is_flag_in_token(self, flag, token, rename=None):
        """Set a flag if it is found in the token's groups field."""
        if token.groups.get(flag):
            flag = rename if rename else flag
            setattr(self, flag, True)

    def flag_from_token(self, flag, token, rename=None):
        """Set a flag if it is found in the token's groups field."""
        value = token.groups.get(flag)
        if value:
            flag = rename if rename else flag
            setattr(self, flag, value.lower())
