"""Build a trait parse result."""

from pylib.shared.util import as_list, squash


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

    def transfer(self, token, names):
        """Move fields from a token to the trait if they exist in the token."""
        for name in names:
            if name in token.groups:
                values = [v.lower() for v in as_list(token.groups[name])]
                setattr(self, name, squash(values))

    def is_flag_in_token(self, token, flag, rename=None):
        """Set a flag if it is found in the token's groups field."""
        if token.groups.get(flag):
            flag = rename if rename else flag
            setattr(self, flag, True)

    def is_flag_missing(self, token, flag, rename=None):
        """Set a flag if it is found in the token's groups field."""
        if not token.groups.get(flag):
            flag = rename if rename else flag
            setattr(self, flag, True)

    def is_value_in_token(self, token, flag, rename=None):
        """Set a flag if it is found in the token's groups field."""
        if value := token.groups.get(flag):
            flag = rename if rename else flag
            setattr(self, flag, value.lower())
