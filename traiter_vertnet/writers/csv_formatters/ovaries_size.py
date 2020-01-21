"""Format the trait for CSV output."""

import traiter_vertnet.writers.csv_formatters.gonad_size as gonad_size


def csv_formatter(_, row, traits):
    """Format the trait for CSV output."""
    if not traits:
        return
    records = gonad_size.build_records(traits)
    records = gonad_size.merge_records(records)
    gonad_size.format_records(records, row, 'ovaries')
