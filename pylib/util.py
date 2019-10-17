"""Misc utilities."""

import re
import inflect

FLAGS = re.IGNORECASE | re.VERBOSE
INFLECT = inflect.engine()


def ordinal(i):
    """Convert the digit to an ordinal value: 1->1st, 2->2nd, etc."""
    return INFLECT.ordinal(i)


def number_to_words(number):
    """Convert the number or ordinal value into words."""
    return INFLECT.number_to_words(number)
