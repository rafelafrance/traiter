import os
from contextlib import contextmanager
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import Any
from typing import Generator

import ftfy
import inflect
import regex as re

INFLECT = inflect.engine()


@contextmanager
def get_temp_dir(
    prefix: str = "temp_", where: str | Path | None = None, keep: bool = False
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
    return " ".join(text.split())


def flatten(nested: list) -> list:
    """Flatten an arbitrarily nested list."""
    flat = []
    for item in nested:
        if isinstance(item, (list, tuple, set)):
            flat.extend(flatten(list(item)))
        else:
            flat.append(item)
    return flat


def as_list(values: Any) -> list:
    """Convert values to a list."""
    return list(values) if isinstance(values, (list, tuple, set)) else [values]


def to_positive_float(value: str) -> float | None:
    """Convert the value to a float."""
    value = re.sub(r"[^\d./]", "", value) if value else ""
    try:
        return float(value)
    except ValueError:
        return None


def to_positive_int(value: str) -> int | None:
    """Convert the value to an integer."""
    value = re.sub(r"[^\d./]", "", value) if value else ""
    value = re.sub(r"\.$", "", value)
    try:
        return int(value)
    except ValueError:
        return None


def clean_text(
    text: str,
    trans: dict[int, str] | None = None,
    replace: dict[int, str] | None = None,
) -> str:
    """Clean text before trait extraction."""
    text = text if text else ""

    # Handle uncommon mojibake
    if trans:
        text = text.translate(trans)

    if replace:
        for old, new in replace.items():
            text = text.replace(old, new)

    text = " ".join(text.split())  # Space normalize

    # Join hyphenated words when they are at the end of a line
    text = re.sub(r"([a-z])-\s+([a-z])", r"\1\2", text, flags=re.IGNORECASE)

    text = ftfy.fix_text(text)  # Handle common mojibake

    text = re.sub(r"\p{Cc}+", " ", text)  # Remove control characters

    return text
