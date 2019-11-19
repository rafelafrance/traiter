"""Misc. utilities"""


def flatten(nested):
    """Flatten an arbitrarily nested list."""
    flat = []
    nested = nested if isinstance(nested, (list, tuple, set)) else [nested]
    for item in nested:
        if isinstance(item, (list, tuple, set)):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat


def squash(values):
    """Squash a list to a single value is its length is one."""
    return values if len(values) > 1 else values[0]
