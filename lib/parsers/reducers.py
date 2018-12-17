"""Functions for reducing parser results."""

import regex
from lib.lexers.lex_base import Tokens
from lib.parsers.parse_base import Result
import lib.parsers.unit_conversions as conversions


MM = regex.compile('mm | millimeters', regex.IGNORECASE | regex.VERBOSE)


def value_span(stack: Tokens, raw: str, args: dict) -> Result:
    """Handle the case where the value spans one or more tokens."""
    span = args['span']

    start = stack[span[0]].start
    if len(span) == 1:
        end = stack[span[0]].end
    else:
        end = stack[span[1]].end

    value = raw[start:end]

    return Result(value=value, start=stack[0].start, end=stack[-1].end)


def strip_span(stack: Tokens, raw: str, args: dict) -> Result:
    """Trim characters from a value_span."""
    result = value_span(stack, raw, args)

    match = regex.match(f"^{args['strip']}(.*?){args['strip']}$", result.value)

    return Result(value=match[1], start=result.start, end=result.end)


def len_in_key(stack: Tokens, raw: str, args: dict) -> Result:
    """Pull the length units from the key."""
    start = stack[args['value']].start
    end = stack[args['value']].end
    value = float(raw[start:end])

    return Result(
        value=value, inferred=False, start=stack[0].start, end=stack[-1].end)


def key_len_units(stack: Tokens, raw: str, args: dict) -> Result:
    """Key, length, & units are in separate tokens."""
    start = stack[args['units']].start
    end = stack[args['units']].end
    units = raw[start:end]

    start = stack[args['value']].start
    end = stack[args['value']].end
    value = float(raw[start:end]) * conversions.LENGTH[units]

    return Result(
        value=value, inferred=False, start=stack[0].start, end=stack[-1].end)
