"""Functions for reducing parser results."""

import regex
from lib.lexers.lex_base import Tokens
from lib.parsers.parse_base import Result
import lib.parsers.unit_conversions as conv


MM = regex.compile('mm | millimeters', regex.IGNORECASE | regex.VERBOSE)
SHORTHAND = regex.compile(r'[:/-]', regex.VERBOSE)
RANGE = regex.compile(r' - | to ', regex.VERBOSE)
FRACTION = regex.compile(r' \/ ', regex.VERBOSE)


def convert_units(value: float, units: str) -> float:
    """Normalize the units to millimeters or grams."""
    factor = conv.UNITS[units.lower()]
    if isinstance(value, list):
        value = [round(v * factor, 2) for v in value]
    else:
        value *= factor
        value = round(value, 2)
    return value


def token_to_str(stack: Tokens, raw: str, idx: int) -> str:
    """Get the string the token represents."""
    start = stack[idx].start
    end = stack[idx].end
    return raw[start:end]


def token_to_strings(stack: Tokens, raw: str, idx: int, regexp) -> str:
    """Get the string the token represents."""
    return [s for s in regexp.split(token_to_str(stack, raw, idx))]


def to_float(value):
    """Convert string to float."""
    try:
        return float(value)
    except ValueError:
        return None


def token_to_float(stack: Tokens, raw: str, idx: int) -> str:
    """Get the float value the token represents."""
    text = token_to_str(stack, raw, idx)
    return to_float(text)


def token_to_floats(stack, raw, idx, regexp=RANGE, as_array=False):
    """Get the float value the token represents."""
    text = token_to_str(stack, raw, idx)
    texts = regexp.split(text)
    values = [to_float(t) for t in texts]
    return values[0] if len(values) == 1 and not as_array else values


def value_span(stack: Tokens, raw: str, args: dict) -> Result:
    """Handle the case where the value spans one or more tokens.

    args:
        span: tuple with (index of first value token, last token)
    """
    span = args['span']
    start = stack[span[0]].start

    if len(span) == 1:
        end = stack[span[0]].end
    else:
        end = stack[span[1]].end

    value = raw[start:end]

    return Result(value=value, start=stack[0].start, end=stack[-1].end)


def strip_span(stack: Tokens, raw: str, args: dict) -> Result:
    """Trim characters from a value_span.

    args:
        span:   tuple with (index of first value token, last token)
        strip:  regex for what to strip off the start and end of the value
    """
    result = value_span(stack, raw, args)

    match = regex.match(f"^{args['strip']}(.*?){args['strip']}$", result.value)

    return Result(value=match[1], start=result.start, end=result.end)


def len_units_in_key(stack: Tokens, raw: str, args: dict) -> Result:
    """Pull the length units from the key.

    args:
        key:    index of token with the key
        value:  index of token with the value
    """
    value = token_to_floats(stack, raw, args['value'])
    return Result(
        value=value, has_units=True, start=stack[0].start, end=stack[-1].end)


def length(stack: Tokens, raw: str, args: dict) -> Result:
    """Key, length, & units are in separate tokens.

    args:
        value:  index of token with the value
        units:  index of token with the length units
    """
    ambiguous = args.get('ambiguous', False)
    has_units = True if args.get('units') else False
    units = token_to_str(stack, raw, args['units']) if has_units else ''

    value = token_to_floats(stack, raw, args['value'])
    value = convert_units(value, units)

    return Result(
        value=value,
        has_units=has_units,
        ambiguous=ambiguous,
        start=stack[0].start,
        end=stack[-1].end)


def shorthand(stack: Tokens, raw: str, args: dict) -> Result:
    """Handle shorthand notation like 11-22-33-44:55.

    Which is total-tail-hindFoot-ear-mass.
    First 4 are lengths & mass is optional.
    args:
        value:  index of token with the values
        part:   wihich part of 11-22-33-44:55 notation holds the value
    """
    values = token_to_floats(stack, raw, args['value'], SHORTHAND)
    value = values[args['part']] if len(values) > args['part'] else None
    return Result(
        value=value, has_units=True, start=stack[0].start, end=stack[-1].end)


def english_len(stack: Tokens, raw: str, args: dict) -> Result:
    """Handle a pattern like: total length: 4 ft 8 in

    Both the feet and inches part can be a range.
    args:
        feet:   index of token with the feet part of the measurement
        inches: index of token with the inches (range?) part of the measurement
    """
    feet = token_to_floats(stack, raw, args['feet'], as_array=True)
    inches = token_to_floats(stack, raw, args['inches'], as_array=True)
    values = [convert_units(f, 'feet') + convert_units(i, 'inches')
              for f in feet for i in inches]
    value = values if len(values) > 1 else values[0]

    return Result(
        value=value, has_units=True, start=stack[0].start, end=stack[-1].end)


def fraction(stack: Tokens, raw: str, args: dict) -> Result:
    """Handle fractional values like 10 3/8 inches."""
    units = token_to_str(stack, raw, args['units'])
    ambiguous = args.get('ambiguous', False)

    value = token_to_str(stack, raw, args['value'])
    parts = value.split()
    whole = to_float(parts[0] if len(parts) > 1 else '0')
    numerator, denominator = [to_float(f) for f in FRACTION.split(parts[-1])]
    value = convert_units(whole + numerator / denominator, units)

    return Result(
        value=value,
        ambiguous=ambiguous,
        has_units=True,
        start=stack[0].start, end=stack[-1].end)
