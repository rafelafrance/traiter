"""Build a trait parse result."""


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
