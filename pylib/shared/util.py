"""Misc. utilities."""

import regex

__VERSION__ = '0.5.0'

FLAGS = regex.VERBOSE | regex.IGNORECASE

BATCH_SIZE = 1_000_000  # How many records to work with at a time


def shorten(text):
    """Collapse whitespace in a string."""
    return ' '.join(text.split())


def flatten(nested):
    """Flatten an arbitrarily nested list."""
    flat = []
    nested = nested if isinstance(nested, (list, tuple, set)) else [nested]
    for item in nested:
        if hasattr(item, '__iter__'):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat


def squash(values):
    """Squash a list to a single value is its length is one."""
    return values if len(values) != 1 else values[0]


def as_list(values):
    """Convert values to a list."""
    return values if isinstance(values, (list, tuple, set)) else [values]


def to_float(value):
    """Convert the value to a float."""
    value = regex.sub(r'[^\d.]', '', value) if value else ''
    try:
        return float(value)
    except ValueError:
        return None


def to_int(value):
    """Convert value to an integer, handle 'no' or 'none' etc."""
    value = regex.sub(r'\D', '', value) if value else ''
    try:
        return int(value)
    except ValueError:
        return 0
