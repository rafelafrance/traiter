def flatten(nested: list) -> list:
    """Flatten an arbitrarily nested list."""
    flat = []
    for item in nested:
        if isinstance(item, (list, tuple, set)):
            flat.extend(flatten(list(item)))
        else:
            flat.append(item)
    return flat
