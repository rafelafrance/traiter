"""Format the trait for CSV output."""

import pylib.vertnet.writers.csv_formatters.gonad_state as gonad_state


def csv_formatter(trait_name, row, traits):
    """Format the trait for CSV output."""
    gonad_state.csv_formatter(trait_name, row, traits, 'ovaries')
