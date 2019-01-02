"""Read the traiter input from a CSV file."""

import csv
from lib.readers.base_reader import BaseReader


class CsvReader(BaseReader):
    """Read the traiter input from a file."""

    def __init__(self, args):
        """Build the reader."""
        self.args = args
        self.reader = None
        self.infile = args.infile
        self.columns = args.csv_columns + args.csv_extra_columns

    def __enter__(self):
        """Use the reader in with statements."""
        self.reader = csv.DictReader(self.infile)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the file handle."""
        self.infile.close()  # paranoia

    def __iter__(self):
        """Loop thru the file."""
        for row in self.reader:
            cols = {k: v for k, v in row.items() if k in self.columns}
            yield cols
