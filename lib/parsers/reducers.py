"""Functions for reducing parser results."""

from dataclasses import dataclass
from typing import Any
import regex


@dataclass
class Result:
    value: Any
    start: int = 0
    end: int = 0


def value_span(stack, raw, args):
    """Handle the case where the value spans one or more tokens."""
    span = args['span']

    start = stack[span[0]].start
    if len(span) == 1:
        end = stack[span[0]].end
    else:
        end = stack[span[1]].end

    value = raw[start:end]

    return Result(value=value, start=stack[0].start, end=stack[-1].end)


def strip_span(stack, raw, args):
    """Trim characters from a value_span."""
    result = value_span(stack, raw, args)

    match = regex.match(f"^{args['strip']}(.*?){args['strip']}$", result.value)

    return Result(value=match[1], start=result.start, end=result.end)
