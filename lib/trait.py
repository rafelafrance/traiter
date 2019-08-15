"""Build a parser trait result."""

from collections import namedtuple


TraitKey = namedtuple('TraitKey', 'value side')


class Trait:
    """Build a parse result."""

    def __init__(self, **kwargs):
        """Build a trait."""
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __repr__(self):
        """Represent the result."""
        return '{}({})'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        """Compare trait_builders for testing."""
        return self.__dict__ == other.__dict__

    def __setattr__(self, name, value):
        """Allow arbitrary attributes on a trait."""
        self.__dict__[name] = value

    def __getattr__(self, name):
        """Handle uninitialized attributes by returning a falsy value."""
        return ''

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

    def merge_flags(self, other):
        """Capture the meaning across all parses."""
        self.ambiguous_key &= other.ambiguous_key

    def as_key(self):
        """Used to tell if the traits are the same trait."""
        return TraitKey(value=self.value, side=self.side)
