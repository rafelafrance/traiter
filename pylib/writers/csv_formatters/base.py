"""Format the trait for CSV output."""

from pylib.util import ordinal


def csv_formatter(trait_name, row, traits):
    """Format the trait for CSV output."""
    records = {}
    for trait in traits:
        key = trait.as_key()
        if key not in records:
            records[key] = trait

    for i, trait in enumerate(records.values(), 1):
        row[f'{trait_name}:{ordinal(i)}_{trait_name}'] = trait.value
