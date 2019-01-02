"""Read the traiter input from a CSV file."""

import csv
from lib.readers.base_reader import BaseReader


class CsvReader(BaseReader):
    """Read the traiter input from a file."""

    def __init__(self, args):
        """Build the reader."""
        self.args = args
        self.reader = None

    def __enter__(self):
        """Use the reader in with statements."""
        print('__enter__')
        self.reader = csv.DictReader(self.args.infile)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the file handle."""
        self.args.infile.close()  # paranoia
        print('__exit__')

    def __iter__(self):
        """Loop thru the file."""
        yield from self.reader
        yield '__done__'
