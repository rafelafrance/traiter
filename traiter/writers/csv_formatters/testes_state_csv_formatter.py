"""Format the trait for CSV output."""

from traiter.util import ordinal


def csv_formatter(trait_name, row, traits):
    """Format the trait for CSV output."""
    if not traits:
        return

    values = []
    for trait in traits:
        value = trait.value.lower()
        if value not in values:
            values.append(value)

    for i, value in enumerate(values, 1):
        row[f'testes_{i}10:{ordinal(i)}_{trait_name}'] = value
