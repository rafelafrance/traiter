"""Write the traiter output to a CSV file."""

import csv
import json
from lib.writers.base_writer import BaseWriter


class CsvWriter(BaseWriter):
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        super().__init__(args)
        self.writer = None
        self.columns = args.extra_field
        self.columns += ['parsed_record']
        self.columns += args.search_field
        self.columns += sorted({f for fds in args.as_is.values() for f in fds})

    def start(self):
        """Start the report."""
        self.writer = csv.DictWriter(self.outfile, self.columns)
        self.writer.writeheader()

    def record(self, raw_record, parsed_record):
        """Output a row to the file."""
        row = {c: raw_record.get(c, '') for c in self.columns}
        row['parsed_record'] = json.dumps(parsed_record)
        self.writer.writerow(row)

    def end(self):
        """End the report."""
