"""Functions for reducing parser results."""

import re


def value_span(stack, raw, args):
    """Handle the case where the value spans one or more tokens."""
    span = args['span']

    if len(span) == 1:
        value = stack[span[0]]['value']
    else:
        value = raw[stack[span[0]]['start']:stack[span[1]]['end']]

    return {'value': value,
            'start': stack[0]['start'],
            'end': stack[-1]['end']}


def strip_span(stack, raw, args):
    """Trim characters from a value_span."""
    result = value_span(stack, raw, args)

    match = re.match(
        f"^{args['strip']}(.*?){args['strip']}$",
        result['value'])

    return {'value': match[1],
            'start': result['start'],
            'end': result['end']}
