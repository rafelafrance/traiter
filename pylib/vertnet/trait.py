"""Build a trait parse result."""

from collections import namedtuple
import pylib.shared.trait as trait

TraitKey = namedtuple('TraitKey', 'value side')


class Trait(trait.Trait):
    """Build a parse result."""

    def merge_ambiguous_key(self, other):
        """Capture the meaning across all parses."""
        ambiguous_key = bool(getattr(self, 'ambiguous_key'))
        ambiguous_key &= bool(getattr(other, 'ambiguous_key'))
        setattr(self, 'ambiguous_key', ambiguous_key)

    def as_key(self):
        """Determine if the traits are the same trait."""
        return TraitKey(value=self.value, side=self.side)
