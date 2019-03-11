"""Read the traiter input from a CSV file."""

import csv
from lib.readers.base_reader import BaseReader


class CsvReader(BaseReader):
    """Read the traiter input from a file."""

    def __init__(self, args):
        """Build the reader."""
        super().__init__(args)
        self.args = args
        self.reader = None
        self.input_file = args.input_file
        self.columns = args.search_field + args.extra_field
        for _, fields in args.as_is.items():
            self.columns += fields

    def __enter__(self):
        """Use the reader in with statements."""
        self.reader = csv.DictReader(self.input_file)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the file handle."""
        self.input_file.close()  # paranoia

    def __iter__(self):
        """Loop thru the file."""
        for row in self.reader:
            cols = {k: v for k, v in row.items() if k in self.columns}
            yield cols
