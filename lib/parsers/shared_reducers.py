"""Functions for reducing parser results."""

# pylint: disable=unused-argument

import regex
from lib.lexers.lex_base import Tokens
from lib.parsers.parse_base import Result
import lib.lexers.shared_regex as regexp
import lib.parsers.shared_unit_conversions as conv


SHORTHAND_SEP = regexp.compile_regex('shorthand_sep')
RANGE_SEP = regexp.compile_regex('range_sep')
FRACTION = regex.compile(r' \/ ', regex.VERBOSE)

DEFINES = regexp.build_regex_defines(regexp.ALL)

SHORTHAND_WT = regex.compile(
    (f'{DEFINES} '
     r'(?&shorthand_vals) (?&shorthand_wt_sep) \s* '
     r'(?P<value> (?&shorthand_val) ) \s* '
     r'(?P<units> (?&metric_wt) )?'),
    regex.VERBOSE | regex.IGNORECASE)


def convert_units(value: float, units: str) -> float:
    """Normalize the units to millimeters or grams."""
    factor = conv.UNITS[units.lower()]
    if isinstance(value, list):
        value = [round(v * factor, 2) for v in value]
    else:
        value *= factor
        value = round(value, 2)
    return value


def token_to_str(stack: Tokens, text: str, idx: int) -> str:
    """Get the string the token represents."""
    start = stack[idx].start
    end = stack[idx].end
    return text[start:end]


def token_to_strings(stack: Tokens, text: str, idx: int, regexp) -> str:
    """Get the string the token represents."""
    return [s for s in regexp.split(token_to_str(stack, text, idx))]


def to_float(value):
    """Convert string to float."""
    value = value.replace(',', '')
    try:
        return float(value)
    except ValueError:
        return None


def token_to_float(stack: Tokens, text: str, idx: int) -> str:
    """Get the float value the token represents."""
    text = token_to_str(stack, text, idx)
    return to_float(text)


def token_to_floats(stack, text, idx, regexp=RANGE_SEP, as_array=False):
    """Get the float value the token represents."""
    text = token_to_str(stack, text, idx)
    texts = regexp.split(text)
    values = [to_float(t) for t in texts]
    return values[0] if len(values) == 1 and not as_array else values


def value_span(stack: Tokens, text: str, args: dict) -> Result:
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

    value = text[start:end]

    return Result(value=value, start=stack[0].start, end=stack[-1].end)


def strip_span(stack: Tokens, text: str, args: dict) -> Result:
    """Trim characters from a value_span.

    args:
        span:   tuple with (index of first value token, last token)
        strip:  regex for what to strip off the start and end of the value
    """
    result = value_span(stack, text, args)

    match = regex.match(f"^{args['strip']}(.*?){args['strip']}$", result.value)

    return Result(value=match[1], start=result.start, end=result.end)


def len_units_in_key(stack: Tokens, text: str, args: dict) -> Result:
    """Pull the length units from the key.

    args:
        key:    index of token with the key
        value:  index of token with the value
    """
    value = token_to_floats(stack, text, args['value'])
    return Result(
        value=value, has_units=True, start=stack[0].start, end=stack[-1].end)


def numeric_units(stack: Tokens, text: str, args: dict) -> Result:
    """Key, value, & units are in separate tokens.

    args:
        value:  index of token with the value
        units:  index of token with the length units
    """
    ambiguous = args.get('ambiguous', False)
    has_units = bool(args.get('units'))
    units = token_to_str(stack, text, args['units']) if has_units else ''

    value = token_to_floats(stack, text, args['value'])
    value = convert_units(value, units)

    return Result(
        value=value,
        has_units=has_units,
        ambiguous=ambiguous,
        start=stack[0].start,
        end=stack[-1].end)


def shorthand(stack: Tokens, text: str, args: dict) -> Result:
    """Handle shorthand notation like 11-22-33-44:55g.

    Which is total-tail-hindFoot-ear-mass.
    First 4 are lengths & mass is optional.
    args:
        value:  index of token with the values
        part:   which part of 11-22-33-44:55 notation holds the value
    """
    values = token_to_floats(stack, text, args['value'], SHORTHAND_SEP)
    value = values[args['part']] if len(values) > args['part'] else None
    return Result(
        value=value, has_units=True, start=stack[0].start, end=stack[-1].end)


def shorthand_mass(stack: Tokens, text: str, args: dict) -> Result:
    """Handle shorthand notation like 11-22-33-44:55g.

    Which is total-tail-hindFoot-ear-mass. The token has the mass in this case.
    args:
        value:  index of token with the values
    """
    all = token_to_str(stack, text, args['value'])
    match = SHORTHAND_WT.match(all)
    value = to_float(match.group('value'))
    units = match.group('units')
    if value is None:
        has_units = None
    else:
        value = convert_units(value, units)
        has_units = bool(units)

    return Result(
        value=value,
        has_units=has_units,
        start=stack[0].start, end=stack[-1].end)


def english_units(stack: Tokens, text: str, args: dict) -> Result:
    """Handle a pattern like: total length: 4 ft 8 in.

    Also handle 4 lbs 9 ozs.
    Both the numeric parts can be a range.
    args:
        start: index of token with the first value
    """
    ambiguous = args.get('ambiguous', False)
    idx = args['start']
    major = token_to_floats(stack, text, idx + 0, as_array=True)
    minor = token_to_floats(stack, text, idx + 2, as_array=True)
    major_units = token_to_str(stack, text, idx + 1)
    minor_units = token_to_str(stack, text, idx + 3)
    values = [convert_units(f, major_units) + convert_units(i, minor_units)
              for f in major for i in minor]
    value = values if len(values) > 1 else values[0]

    return Result(
        value=value,
        ambiguous=ambiguous,
        has_units=True,
        start=stack[0].start,
        end=stack[-1].end)


def fraction(stack: Tokens, text: str, args: dict) -> Result:
    """Handle fractional values like 10 3/8 inches."""
    units = token_to_str(stack, text, args['units'])
    ambiguous = args.get('ambiguous', False)

    value = token_to_str(stack, text, args['value'])
    parts = value.split()
    whole = to_float(parts[0] if len(parts) > 1 else '0')
    numerator, denominator = [to_float(f) for f in FRACTION.split(parts[-1])]
    value = convert_units(whole + numerator / denominator, units)

    return Result(
        value=value,
        ambiguous=ambiguous,
        has_units=True,
        start=stack[0].start, end=stack[-1].end)
