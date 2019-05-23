"""Misc utilities."""

import inflect

INFLECT = inflect.engine()


def ordinal(i):
    """Convert the digit to an ordinal value: 1->1st, 2->2nd, etc."""
    return INFLECT.ordinal(i)
