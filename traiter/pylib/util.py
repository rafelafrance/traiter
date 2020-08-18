"""Misc. utilities."""

import os
from contextlib import contextmanager
from datetime import datetime
from shutil import rmtree
from tempfile import mkdtemp

import inflect
import regex as re

__VERSION__ = '0.8.0'

FLAGS = re.VERBOSE | re.IGNORECASE

BATCH_SIZE = 1_000_000  # How many records to work with at a time

INFLECT = inflect.engine()


class DotDict(dict):
    """Allow dot.notation access to dictionary items"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def log(msg):
    """Log a status message."""
    print(f'{now()} {msg}')


def now():
    """Generate a timestamp."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def today():
    """Get today's date."""
    return now()[:10]


@contextmanager
def get_temp_dir(prefix, where=None, keep=False):
    """Handle creation and deletion of temporary directory."""
    if where and not os.path.exists(where):
        os.mkdir(where)

    temp_dir = mkdtemp(prefix=prefix, dir=where)
    # os.environ['SQLITE_TMPDIR'] = temp_dir

    try:
        yield temp_dir
    finally:
        if not keep or not where:
            rmtree(temp_dir)


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


def as_set(values):
    """Convert values to a list."""
    settable = isinstance(values, (list, tuple, set))
    return set(values) if settable else {values}


def as_tuple(values):
    """Convert values to a tuple."""
    return values if isinstance(values, tuple) else tuple(values)


def as_member(values):
    """Convert values to set members (hashable)."""
    return tuple(values) if isinstance(values, (list, set)) else values


def to_positive_float(value):
    """Convert the value to a float."""
    value = re.sub(r'[^\d./]', '', value) if value else ''
    try:
        return float(value)
    except ValueError:
        return None


def to_positive_int(value):
    """Convert the value to an integer."""
    value = re.sub(r'[^\d./]', '', value) if value else ''
    value = re.sub(r'\.$', '', value)
    try:
        return int(value)
    except ValueError:
        return None


def camel_to_snake(name):
    """Convert a camel case string to snake case."""
    split = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', split).lower()


def ordinal(i):
    """Convert the digit to an ordinal value: 1->1st, 2->2nd, etc."""
    return INFLECT.ordinal(i)


def number_to_words(number):
    """Convert the number or ordinal value into words."""
    return INFLECT.number_to_words(number)


def filter_matches(matches):
    """Filter a sequence of matches so they don't contain overlaps.

    Matches: array of tuples: [(match_id, start, end), ...]
    """
    if not matches:
        return []
    first, *rest = sorted(matches, key=lambda m: (m[1], -m[2]))
    cleaned = [first]
    for match in rest:
        if match[1] >= cleaned[-1][2]:
            cleaned.append(match)
    return cleaned


def clean_text(text):
    """Strip control characters from improperly encoded input strings."""
    text = text if text else ''
    return re.sub(r'\p{Cc}+', ' ', text)
