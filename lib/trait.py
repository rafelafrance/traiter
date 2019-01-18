"""Build a parser trait result."""

# pylint: disable=too-many-arguments,too-many-instance-attributes

from lib.numeric_trait_mixin import NumericTraitMixIn


class Trait(NumericTraitMixIn):
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
        """Compare traits."""
        return self.as_dict() == other.as_dict()

    def is_flag_in_token(self, flag, token, rename=None):
        """Set a flag if it is found in the token's groups field."""
        if token.groups.get(flag):
            flag = rename if rename else flag
            self.flags[flag] = True

    def flag_from_token(self, flag, token, rename=None):
        """Set a flag if it is found in the token's groups field."""
        value = token.groups.get(flag)
        if value:
            flag = rename if rename else flag
            self.flags[flag] = value.lower()
