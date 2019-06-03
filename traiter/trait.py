"""Build a parser trait result."""


class Trait:
    """Build a parse result."""

    def __init__(self, **kwargs):
        """Build a trait.

        value:           Normalized value

        field:           What field contained the trait
        start:           Starting index for the trait
        end:             Ending index for the trait

        as_is:           Sometimes we take an entire cell as-is
        ambiguous_key:   Abbreviations can be ambiguous
        side:            Left, right, 1, 2, etc.

        skipped:         If the trait is skipped, why
        """
        self.value = kwargs.get('value', None)

        self.field = kwargs.get('field', '')
        self.start = kwargs.get('start', 0)
        self.end = kwargs.get('end', 0)

        self.as_is = kwargs.get('as_is', False)
        self.ambiguous_key = kwargs.get('ambiguous_key', False)

        self.side = kwargs.get('side', '')

        self.skipped = ''

    def __repr__(self):
        """Represent the result."""
        return '{}({})'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        """Compare trait_builders for testing."""
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

    def merge_flags(self, other):
        """Capture the meaning across all parses."""
        self.ambiguous_key &= other.ambiguous_key
