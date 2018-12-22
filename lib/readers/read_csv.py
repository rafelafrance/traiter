"""Read the traiter input from a CSV file."""

import csv


class ReadCsv:
    """Read the traiter input from a file."""

    def __init__(self, args):
        """Build the reader."""
        self.args = args
        self.reader = None

    def __enter__(self):
        """Use the reader in with statements."""
        self.reader = csv.DictReader(self.args.infile)
        return self.reader

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the file handle."""
        pass

    def __iter__(self):
        """Loop thru the file."""
        return self

    def next(self):
        """Get the next row."""
