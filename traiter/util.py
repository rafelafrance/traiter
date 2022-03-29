"""Misc. utilities shared between client Traiters."""

import os
from contextlib import contextmanager
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import Any, Generator, Hashable, Optional, Union

import ftfy
import inflect
import regex as re

INFLECT = inflect.engine()

FLAGS = re.IGNORECASE | re.VERBOSE


class DotDict(dict):
    """Allow dot.notation access to dictionary items."""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


@contextmanager
def get_temp_dir(
        prefix: str = 'temp_',
        where: Optional[Union[str, Path]] = None,
        keep: bool = False
) -> Generator:
    """Handle creation and deletion of temporary directory."""
    if where and not os.path.exists(where):
        os.mkdir(where)

    temp_dir = mkdtemp(prefix=prefix, dir=where)

    try:
        yield temp_dir
    finally:
        if not keep or not where:
            rmtree(temp_dir)


def shorten(text: str) -> str:
    """Collapse whitespace in a string."""
    return ' '.join(text.split())


def flatten(nested: Any) -> list:
    """Flatten an arbitrarily nested list."""
    flat = []
    nested = nested if isinstance(nested, (list, tuple, set)) else [nested]
    for item in nested:
        # if not isinstance(item, str) and hasattr(item, '__iter__'):
        if isinstance(item, (list, tuple, set)):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat


def squash(values: Union[list, set]) -> Any:
    """Squash a list to a single value if its length is one."""
    return list(values) if len(values) != 1 else values[0]


def as_list(values: Any) -> list:
    """Convert values to a list."""
    return list(values) if isinstance(values, (list, tuple, set)) else [values]


def as_set(values: Any) -> set:
    """Convert values to a set."""
    return set(values) if isinstance(values, (list, tuple, set)) else {values}


def as_tuple(values: Any) -> tuple[Any, ...]:
    """Convert values to a tuple."""
    return tuple(values) if isinstance(values, (list, tuple, set)) else (values,)


def as_member(values: Any) -> Hashable:
    """Convert values to set members (hashable)."""
    return tuple(values) if isinstance(values, (list, set)) else values


def to_positive_float(value: str):
    """Convert the value to a float."""
    value = re.sub(r'[^\d./]', '', value) if value else ''
    try:
        return float(value)
    except ValueError:
        return None


def to_positive_int(value: str):
    """Convert the value to an integer."""
    value = re.sub(r'[^\d./]', '', value) if value else ''
    value = re.sub(r"\.$", '', value)
    try:
        return int(value)
    except ValueError:
        return None


def camel_to_snake(name: str) -> str:
    """Convert a camel case string to snake case."""
    split = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', split).lower()


def ordinal(i: str) -> str:
    """Convert the digit to an ordinal value: 1->1st, 2->2nd, etc."""
    return INFLECT.ordinal(i)


def number_to_words(number: str) -> str:
    """Convert the number or ordinal value into words."""
    return INFLECT.number_to_words(number)


def clean_text(
        text: str,
        trans: Optional[dict[int, str]] = None,
        replace: Optional[dict[str, str]] = None,
) -> str:
    """Clean text before trait extraction."""
    text = text if text else ''

    # Handle uncommon mojibake
    if trans:
        text = text.translate(trans)
    if replace:
        for old, new in replace.items():
            text = text.replace(old, new)

    text = ' '.join(text.split())  # Space normalize

    # Join hyphenated words when they are at the end of a line
    text = re.sub(r'([a-z])-\s+([a-z])', r'\1\2', text, flags=re.IGNORECASE)

    text = ftfy.fix_text(text)  # Handle common mojibake

    text = re.sub(r'\p{Cc}+', ' ', text)  # Remove control characters

    return text


def xor(one: Any, two: Any) -> bool:
    """Emulate a logical xor."""
    return (not one and two) or (one and not two)


def sign(x: Union[int, float]) -> int:
    """Return the sign of a number (-1, 0, 1)."""
    return 0 if x == 0 else (-1 if x < 0 else 1)


def list_to_re_choice(values):
    """Convert a list of values into a regex choice."""
    values = sorted(values, key=lambda v: -len(v))
    values = [re.escape(v) for v in values]
    pattern = '|'.join(values)
    pattern = fr'({pattern})'
    return pattern


def list_to_char_class(values):
    """Convert a list of values into a regex character class."""
    values = sorted(values, key=lambda v: -len(v))
    values = [re.escape(v) for v in values]
    pattern = ''.join(values)
    pattern = fr'[{pattern}]'
    return pattern
