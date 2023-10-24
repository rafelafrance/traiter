from typing import Any, Union

import ftfy
import regex as re


def shorten(text: str) -> str:
    """Collapse whitespace in a string."""
    return " ".join(text.split())


def compress(text: str) -> str:
    """Collapse whitespace in a string but keep lines."""
    text = [" ".join(ln.split()) for ln in text.splitlines()]
    text = "\n".join(ln for ln in text if ln)
    return text


def as_list(values: Any) -> list:
    """Convert values to a list."""
    return list(values) if isinstance(values, (list, tuple, set)) else [values]


def to_positive_float(value: str) -> Union[float, None]:
    """Convert the value to a float."""
    value = re.sub(r"[^\d./]", "", value) if value else ""
    try:
        return float(value)
    except ValueError:
        return None


def to_positive_int(value: str) -> Union[int, None]:
    """Convert the value to an integer."""
    value = re.sub(r"[^\d./]", "", value) if value else ""
    value = re.sub(r"\.$", "", value)
    try:
        return int(value)
    except ValueError:
        return None


def clean_text(
    text: str,
    trans: Union[dict[int, str], None] = None,
    replace: Union[dict[str, str], None] = None,
) -> str:
    """Clean text before trait extraction."""
    text = text if text else ""

    # Handle uncommon mojibake
    if trans:
        text = text.translate(trans)

    if replace:
        for old, new in replace.items():
            text = text.replace(old, new)

    text = shorten(text)  # Space normalize

    # Join hyphenated words when they are at the end of a line
    text = re.sub(r"([a-z])-\s+([a-z])", r"\1\2", text, flags=re.IGNORECASE)

    text = ftfy.fix_text(text)  # Handle common mojibake

    text = re.sub(r"\p{Cc}+", " ", text)  # Remove control characters

    return text
