"""Build a trait parse result."""

from collections import namedtuple
import pylib.shared.trait as trait


TraitKey = namedtuple('TraitKey', 'value side')


class Trait(trait.Trait):
    """Build a parse result."""

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

    def merge_ambiguous_key(self, other):
        """Capture the meaning across all parses."""
        ambiguous_key = bool(getattr(self, 'ambiguous_key'))
        ambiguous_key &= bool(getattr(other, 'ambiguous_key'))
        setattr(self, 'ambiguous_key', ambiguous_key)

    def as_key(self):
        """Determine if the traits are the same trait."""
        return TraitKey(value=self.value, side=self.side)
